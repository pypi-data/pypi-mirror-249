import logging
import warnings
from dataclasses import asdict
from typing import Callable, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bayes_opt.util import UtilityFunction, acq_max
from matplotlib import cm
from sklearn.gaussian_process import GaussianProcessRegressor, kernels

from .constants import METRICS, METRICS_MAX, METRICS_MIN
from .ela import vm_features, vm_triples
from .problems.problem import ProblemBase
from .sample import DOE, SampleCached

LOG = logging.getLogger(__name__)


def build_gp_matern(
    x: np.ndarray,
    f: np.ndarray,
    nu: float = 1.5,
    length_scale: float = 1.0,
    length_scale_bounds: Union[str, Tuple[float, float]] = (1e-5, 1e5),
    n_restarts_optimizer: int = 0,
    seed: int = 0,
):
    kernel = kernels.Matern(
        length_scale=length_scale,
        length_scale_bounds=length_scale_bounds,
        nu=nu,
    )
    model = GaussianProcessRegressor(
        kernel=kernel,
        alpha=1e-6,
        normalize_y=True,
        n_restarts_optimizer=n_restarts_optimizer,
        random_state=seed,
    )
    # Sklearn's GP throws a large number of warnings at times, but
    # we don't really need to see them here.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(x, f)
    return model


def calc_suitability(
    model: GaussianProcessRegressor,
    x: np.ndarray,
    f: np.ndarray,
) -> float:
    f_model = model.predict(x)
    if np.isnan(f_model).all():
        # Failed to build model
        return -np.inf, -np.inf
    idx = np.triu_indices(len(x), 1)
    f_diffs = f.reshape(-1, 1) - f.flatten()
    f_diffs_model = f_model.reshape(-1, 1) - f_model
    f_diff_signs = np.sign(np.array(f_diffs[idx]))
    f_diff_signs_model = np.sign(f_diffs_model[idx])
    return np.mean(f_diff_signs == f_diff_signs_model)


def calc_r2_cv(
    model: GaussianProcessRegressor,
    x: np.ndarray,
    f: np.ndarray,
    cv: int = 5,
) -> float:
    from sklearn.model_selection import cross_val_score

    # Sklearn's GP throws a large number of warnings at times, but
    # we don't really need to see them here.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return cross_val_score(model, x, f, cv=cv).mean()


def calc_suggested_max_f(
    problem: ProblemBase,
    model: GaussianProcessRegressor,
    f_max: float,
    utility_function: UtilityFunction = None,
) -> float:
    # The model should be built for maximization, i.e. with -f values
    if utility_function is None:
        utility_function = UtilityFunction()
    suggestion_x = acq_max(
        ac=utility_function.utility,
        gp=model,
        y_max=f_max,
        bounds=np.array([_ for _ in problem.variable_bounds]).T,
        random_state=np.random.RandomState(0),
    )
    # We assume maximization problem, so return negative of real problem value
    return float(-problem.calc(suggestion_x))


def models_estimate(
    problem: ProblemBase,
    metric: METRICS,
    x: np.ndarray,
    f: np.ndarray,
) -> Tuple[List[GaussianProcessRegressor], List[float]]:
    if metric in {METRICS.SUIT_EXT, METRICS.VM_ANGLES_EXT, METRICS.SEGMENT_EXT}:
        triples = vm_triples.collect_space_filling(x, 2 * x.size, symmetric=True)
        vm = vm_features.VariabilityMap(x, f, triples)
        vm_ext = vm.copy_extended(n_splits_min=2, n_splits_max=2)
        vm_ext_seg = vm_features.Segmentation(vm_ext)

    models: List[GaussianProcessRegressor] = []
    metric_values: List[float] = []
    for nu in sorted([0.5, 1.5, 2.5, np.inf] + [1, 2, 3]):
        model = build_gp_matern(x, f, nu=nu, n_restarts_optimizer=5)
        models.append(model)
        if np.isnan(model.predict(x)).all():
            metric_values.append(np.nan)
            continue

        if metric == METRICS.R2_CV:
            metric_value = calc_r2_cv(model, x, f)
        # elif metric == METRICS.SUGGESTED_F:
        #     metric_value = calc_suggested_max_f(problem, model, f.max())
        elif metric == METRICS.SUIT_EXT:
            metric_value = calc_suitability(model, vm_ext.x, vm_ext.f)
        elif metric == METRICS.VM_ANGLES_EXT:
            metric_value = vm_ext.validate(model)
        elif metric == METRICS.SEGMENT_EXT:
            metric_value = vm_ext_seg.validate(model, n_sectors=19)
        else:
            raise ValueError(f"Unknown model selection metric {metric}")

        metric_values.append(metric_value)
    return models, metric_values


def models_select(metric_values: List[float], metric: METRICS) -> int:
    if len(metric_values) == 1:
        return 0

    best_value = None
    best_index = None
    for i, metric_value in enumerate(metric_values):
        if not np.isfinite(metric_value):
            continue

        if best_value is None:
            best_value = metric_value
            best_index = i
        elif metric in METRICS_MIN:
            if metric_value < best_value:
                best_value = metric_value
                best_index = i
        elif metric in METRICS_MAX:
            if metric_value > best_value:
                best_value = metric_value
                best_index = i
        else:
            raise ValueError(f"Can not compare models for metric {metric}")

    assert best_value is not None
    assert best_index is not None
    return best_index


def analyze_sample_features(
    problem_modules: List,
    dim: int,
    sizes: List[int],
    metric: METRICS,
    seed: int,
) -> pd.DataFrame:
    data_rows = []
    for problem_module in problem_modules:
        for size in sizes:
            problem: ProblemBase = problem_module.Problem(dim)
            sample = SampleCached(
                problem,
                size=size,
                doe=DOE.RAND,
                options={"seed": seed},
            )
            sample_features = sample.features
            models_info = sample.models_by_metric[metric]
            best_i = models_select([m.metric_value for m in models_info], metric)
            best_model_info = asdict(models_info[best_i])
            data_rows.append(
                pd.Series(
                    {
                        # Problem definition
                        "problem_id": problem.id,
                        "problem": problem.NAME,
                        "dim": dim,
                        "size": size,
                        "seed": seed,
                        "metric": metric,
                        **sample_features,
                        **best_model_info,
                    }
                )
            )
    return pd.DataFrame(data_rows)


def plot_surface(
    func: Callable[[np.ndarray], np.ndarray],
    lower_bound: Tuple[float, float],
    upper_bound: Tuple[float, float],
    n_nodes_x1: int = 50,
    n_nodes_x2: int = 50,
    n_nodes_f: int = 50,
    contour: bool = False,
    wireframe: bool = False,
    file_name: bool = None,
    title: Optional[str] = None,
    size: Tuple[float, float] = (6, 5),
    dpi: int = 100,
    sample_x: np.ndarray = None,
    sample_f: np.ndarray = None,
    samples: Dict[str, Tuple[np.ndarray, np.ndarray]] = {},
    samples_m: Dict[str, str] = {},  # marker
    samples_c: Dict[str, str] = {},  # color
):
    lb1, lb2 = lower_bound[:2]
    ub1, ub2 = upper_bound[:2]
    x1_nodes = np.linspace(lb1, ub1, n_nodes_x1)
    x2_nodes = np.linspace(lb2, ub2, n_nodes_x2)
    x1_grid, x2_grid = np.meshgrid(x1_nodes, x2_nodes)
    x_grid = np.vstack([x1_grid.flatten(), x2_grid.flatten()]).T
    y_grid = func(x_grid)
    y_grid = np.reshape(y_grid, (x1_grid.shape[0], -1))
    if contour:
        plt.figure(figsize=size, dpi=dpi)
        plt.contourf(x1_grid, x2_grid, y_grid, cmap=cm.coolwarm, levels=n_nodes_f)
        plt.colorbar()
        plt.xlabel("$x_1$")
        plt.ylabel("$x_2$")
        if sample_x is not None:
            sample_x = np.atleast_2d(sample_x)
            plt.plot(sample_x[:, 0], sample_x[:, 1], ".", c="k")
            if sample_f is not None:
                [
                    plt.text(xi[0], xi[1], f"{i}|{fi[0]:.1f}", fontsize=8)
                    for i, (xi, fi) in enumerate(zip(sample_x, sample_f))
                ]
        for label, (x, f) in samples.items():
            x = np.atleast_2d(x)
            plt.plot(
                x[:, 0],
                x[:, 1],
                samples_m.get(label, "."),
                c=samples_c.get(label, None),
                label=label,
            )
            if f is not None:
                [
                    plt.text(xi[0], xi[1], f"{i}|{fi[0]:.1f}", fontsize=8)
                    for i, (xi, fi) in enumerate(zip(x, f))
                ]
    else:
        fig = plt.figure(figsize=size, dpi=dpi)
        ax = fig.add_subplot(projection="3d")
        ax.set_box_aspect(aspect=None, zoom=0.8)
        ax.set_xlabel("$x_1$")
        ax.set_ylabel("$x_2$")
        ax.set_zlabel("$f$")
        if wireframe:
            ax.plot_wireframe(x1_grid, x2_grid, y_grid)
        else:
            ax.plot_surface(x1_grid, x2_grid, y_grid, cmap=cm.coolwarm)
        if sample_x is not None and sample_f is not None:
            sample_x = np.atleast_2d(sample_x)
            sample_f = np.atleast_2d(sample_f)
            ax.scatter3D(sample_x[:, 0], sample_x[:, 1], sample_f[:, 0], ".", c="k")
        for label, (x, f) in samples.items():
            x = np.atleast_2d(x)
            f = np.atleast_2d(f)
            ax.scatter3D(
                x[:, 0],
                x[:, 1],
                f[:, 1],
                samples_m.get(label, "."),
                c=samples_c.get(label, None),
                label=label,
            )
    plt.grid()
    if samples:
        plt.legend()
    if title is not None:
        plt.title(title)
    if file_name is None:
        plt.show()
    else:
        plt.savefig(file_name)
        plt.close()
