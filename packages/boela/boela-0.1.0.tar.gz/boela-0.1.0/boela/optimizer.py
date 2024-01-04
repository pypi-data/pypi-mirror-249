import logging
import time
from typing import Callable, List, Tuple

import numpy as np
import pandas as pd
from bayes_opt import UtilityFunction
from bayes_opt.bayesian_optimization import BayesianOptimization
from bayes_opt.util import UtilityFunction, acq_max

from .constants import METRICS
from .model import build_gp_matern, models_estimate, models_select
from .problems.problem import ProblemBase
from .sample import DOE, SampleCached

LOG = logging.getLogger(__name__)


class Optimizer(BayesianOptimization):
    def __init__(
        self,
        problem: ProblemBase,
        init_xf: Tuple[np.ndarray, np.ndarray],
        metric: METRICS,
        predictor: Callable[[np.ndarray, np.ndarray], Tuple[float, float]],
        *args,
        **kwargs,
    ):
        self.problem = problem
        self.init_x, self.init_f = init_xf
        self.metric = metric
        self.predictor = predictor

        super().__init__(
            f=lambda **kwa: -problem.calc(self.space.params_to_array(kwa))[0][0],
            pbounds={
                f"x[{i}]": bound
                for i, bound in enumerate(zip(*problem.variable_bounds))
            },
            *args,
            **kwargs,
        )

        for x in self.init_x:
            # Do not register f values so that the
            # initial sample is printed to log
            self.probe(x)

        n_init = len(self.init_x)
        # Models history
        self.history_nu = [np.nan] * n_init
        self.history_length_scale = [np.nan] * n_init
        self.history_metric_values = [np.nan] * n_init
        # Values history
        self.history_x = [_.tolist() for _ in self.init_x]
        self.history_f = [_[0] for _ in self.init_f]
        self.history_f_model = [np.nan] * n_init
        self.history_time = [np.nan] * n_init

    def suggest(self, utility_function: UtilityFunction):
        time_start = time.time()

        x, neg_f = self._space.params, self._space.target.reshape(-1, 1)
        if self.metric == METRICS.NONE:
            best_model = build_gp_matern(x, neg_f, nu=2.5, n_restarts_optimizer=5)
            best_metric_value = np.nan
        elif self.metric == METRICS.PREDICTED:
            # We used normal f values for sample feature estimation
            nu = self.predictor(x, -neg_f)
            best_model = build_gp_matern(x, neg_f, nu=nu, n_restarts_optimizer=5)
            best_metric_value = np.nan
        else:
            models, metrics = models_estimate(self.problem, self.metric, x, neg_f)
            best_index = models_select(metrics, self.metric)
            best_model, best_metric_value = models[best_index], metrics[best_index]
        # Models history
        self.history_nu.append(best_model.kernel_.nu)
        self.history_length_scale.append(best_model.kernel_.length_scale)
        self.history_metric_values.append(best_metric_value)

        # Finding argmax of the acquisition function.
        suggestion_x: np.ndarray = acq_max(
            ac=utility_function.utility,
            gp=best_model,
            constraint=self.constraint,
            y_max=self._space.target.max(),
            bounds=self._space.bounds,
            random_state=self._random_state,
        )
        suggestion_f = float(self.problem.calc(suggestion_x))
        suggestion_f_model = float(-best_model.predict([suggestion_x]))

        # Values history
        self.history_x.append(suggestion_x.tolist())
        self.history_f.append(suggestion_f)
        self.history_f_model.append(suggestion_f_model)
        self.history_time.append(time.time() - time_start)

        return self._space.array_to_params(suggestion_x)


def solve_problem(
    problem: ProblemBase,
    n_init: int,
    n_iter: int,
    n_seeds: int,
    metric: METRICS,
    predictor: Callable[[np.ndarray, np.ndarray], Tuple[float, float]] = None,
) -> pd.DataFrame:
    solution_f = problem.solutions[0].f[0] if len(problem.solutions) else np.nan
    n_total = n_init + n_iter

    data_frames: List[pd.DataFrame] = []
    for i in range(n_seeds):
        init_sample = SampleCached(
            problem,
            size=n_init,
            doe=DOE.LHS,
            options={"seed": i},
        )
        optimizer = Optimizer(
            problem=problem,
            init_xf=init_sample.xf,
            metric=metric,
            predictor=predictor,
            # Parent args:
            random_state=i,
            allow_duplicate_points=True,
        )
        optimizer.maximize(init_points=0, n_iter=n_iter)
        best_idx = np.argmin(optimizer.history_f)
        x_best = optimizer.history_x[best_idx]
        f_best = optimizer.history_f[best_idx]
        data_frames.append(
            pd.DataFrame(
                {
                    # Problem definition
                    "problem": [problem.NAME] * n_total,
                    "dim": [problem.dim_x] * n_total,
                    "n_init": [n_init] * n_total,
                    "n_iter": [n_iter] * n_total,
                    "metric": [metric] * n_total,
                    "solution_f": [solution_f] * n_total,
                    # Current run info
                    "seed": [i] * n_total,
                    "iteration": list(range(1, n_init + n_iter + 1)),
                    # Models history
                    "nu": optimizer.history_nu,
                    "length_scale": optimizer.history_length_scale,
                    "metric_values": optimizer.history_metric_values,
                    # Values history
                    "x": optimizer.history_x,
                    "f": optimizer.history_f,
                    "f_model": optimizer.history_f_model,
                    "time": optimizer.history_time,
                    "x_best": [x_best] * n_total,
                    "f_best": [f_best] * n_total,
                }
            )
        )
        LOG.info(f"{problem.id} [{i+1}/{n_seeds}]\tx*={x_best}; " f"f(x*)={f_best}")
    return pd.concat(data_frames, ignore_index=True)
