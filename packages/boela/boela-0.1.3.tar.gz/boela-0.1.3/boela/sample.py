import json
import logging
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from .constants import METRICS, SAMPLE_FEATURE
from .problems.problem import ProblemBase

LOG = logging.getLogger(__name__)


class DOE(StrEnum):
    FF = "sample_ff"
    LHS = "sample_lhs"
    GRID = "sample_grid"
    RAND = "sample_rand"


class MODE(StrEnum):
    AUTO = "auto"
    LOAD = "load"
    GENERATE = "generate"


@dataclass
class ModelInfo:
    nu: float
    length_scale: float
    metric_value: float


def clear_samples_cache():
    path = Path(__file__).parent / "samples"
    for p_path in path.iterdir():
        LOG.debug(f"Deleting {p_path}")
        for s_path in p_path.iterdir():
            s_path.unlink()
        p_path.rmdir()


@dataclass
class Sample:
    id: str
    problem: ProblemBase
    x: np.ndarray
    f: np.ndarray

    def features(self) -> Dict[str, float]:
        features = {
            **self._features(SAMPLE_FEATURE.ELA_META),
            **self._features(SAMPLE_FEATURE.ELA_DISTR),
            **self._features(SAMPLE_FEATURE.DISP),
            **self._features(SAMPLE_FEATURE.IC),
            **self._features(SAMPLE_FEATURE.PCA),
            **self._features(SAMPLE_FEATURE.VARIABILITY_MAP),
        }
        # Remove *.const_runtime features to make results reproducible:
        # - 'disp.costs_runtime'
        # - 'ic.costs_runtime'
        # - 'pca.costs_runtime'
        return {
            f"feature.{f}": val
            for f, val in features.items()
            if "costs_runtime" not in f
        }

    def _features(self, feature: SAMPLE_FEATURE, *args, **kwargs) -> Dict[str, float]:
        return _features_estimate(
            id=self.id,
            x=self.x,
            f=self.f,
            bounds=self.problem.variable_bounds,
            feature=feature,
            *args,
            **kwargs,
        )

    def models_by_metric(self) -> Dict[METRICS, List[ModelInfo]]:
        return {
            metric: _models_estimate(
                id=self.id,
                problem=self.problem,
                x=self.x,
                f=self.f,
                metric=metric,
            )
            for metric in [
                METRICS.R2_CV,
                METRICS.SUIT_EXT,
                METRICS.VM_ANGLES_EXT,
                METRICS.SEGMENT_EXT,
            ]
        }


class SampleCached:
    def __init__(
        self,
        problem: ProblemBase,
        size: int,
        doe: DOE = DOE.RAND,
        mode: MODE = MODE.AUTO,
        options: Optional[dict] = None,
        tag: str = "",
    ):
        options = options or {}
        options["size"] = size
        doe_args_str = " ".join([f"{k}={options[k]}" for k in sorted(options)])

        problem_id = f"{problem.NAME}_{problem.dim_x}_{problem.dim_f}"
        doe_id = f"{doe.lower()} {doe_args_str}"
        self.id = f"{problem_id} {doe_id}"
        self.problem = problem

        file_path = Path(__file__).parent / "samples" / problem_id
        if tag:
            file_path = file_path / tag
        self.path = file_path / f"{doe_id}.csv"

        self.mode = mode
        if mode == MODE.AUTO:
            if self.path.is_file():
                self.sample = _sample_load(self.path, self.id, problem, size)
            else:
                self.sample = _sample_generate(self.id, problem, doe, options)
                _sample_save(self.path, self.sample)
        elif mode == MODE.LOAD:
            self.sample = _sample_load(self.path, self.id, problem, size)
        elif mode == MODE.GENERATE:
            self.sample = _sample_generate(self.id, problem, doe, options)
        else:
            raise ValueError(f"Unknown mode {mode}")

    @property
    def xf(self):
        return self.sample.x, self.sample.f

    @property
    def dim_x(self):
        return self.problem.dim_x

    @property
    def dim_f(self):
        return self.problem.dim_f

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id

    @property
    def features(self) -> Dict[str, float]:
        path = _features_path(self.path)
        if self.mode == MODE.AUTO:
            if path.is_file():
                return _features_load(path)
            else:
                features = self.sample.features()
                _features_save(path, features)
                return features
        elif self.mode == MODE.LOAD:
            return _features_load(path)
        elif self.mode == MODE.GENERATE:
            return self.sample.features()

    @property
    def models_by_metric(self) -> Dict[METRICS, List[ModelInfo]]:
        path = _models_path(self.path)
        if self.mode == MODE.AUTO:
            if path.is_file():
                return _models_load(path)
            else:
                models_by_metric = self.sample.models_by_metric()
                _models_save(path, models_by_metric)
                return models_by_metric
        elif self.mode == MODE.LOAD:
            return _models_load(path)
        elif self.mode == MODE.GENERATE:
            return self.sample.models_by_metric()


def _sample_save(path: Path, sample: Sample) -> None:
    LOG.debug(f"Saving {path}")
    data = np.hstack((sample.x, sample.f))
    header = ",".join(sample.problem.variable_names + sample.problem.objective_names)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(path, data, header=header, delimiter=",", comments="")


def _sample_load(path: Path, id: str, problem: ProblemBase, size: int) -> Sample:
    if not path.is_file():
        raise Exception("Can not find the file " + path)
    LOG.debug(f"Loading {path}")
    data = np.loadtxt(path, dtype=float, skiprows=1, delimiter=",", ndmin=2)
    shape = (size, problem.dim_x + problem.dim_f)
    assert data.shape == shape, "Invalid shape of sample in file"
    return Sample(
        id=id,
        problem=problem,
        x=data[:, 0 : problem.dim_x],
        f=data[:, problem.dim_x : problem.dim_x + problem.dim_f],
    )


def _sample_generate(id: str, problem: ProblemBase, doe: DOE, options: dict) -> Sample:
    LOG.debug(f"Generating {id} {options}")
    x, f = getattr(problem, doe)(**options)
    return Sample(id=id, problem=problem, x=x, f=f)


def _features_path(sample_path: Path, feature: Optional[SAMPLE_FEATURE] = None) -> Path:
    return Path(
        f"{sample_path}.features"
        if feature is None
        else f"{sample_path}.features.{feature}"
    )


def _features_estimate(
    id: str,
    x: np.ndarray,
    f: np.ndarray,
    bounds: Tuple[List[float], List[float]],
    feature: SAMPLE_FEATURE,
    *args,
    **kwargs,
) -> dict:
    from .ela import analyze_sample

    if feature not in SAMPLE_FEATURE:
        raise ValueError(f"Features `{feature}` are not available for sample")
    LOG.debug(f"Estimating `{feature}` features of sample {id}")
    f = f.flatten()
    if SAMPLE_FEATURE.bounds_required(feature):
        lb, ub = bounds
        # CM features check for list bound and fail with tuples
        lb, ub = list(lb), list(ub)
        return analyze_sample(feature, x, f, lb, ub, *args, **kwargs)
    else:
        return analyze_sample(feature, x, f, *args, **kwargs)


def _features_save(path: Path, features: dict) -> None:
    LOG.debug(f"Saving {path}")
    with path.open("w") as file:
        json.dump(features, file, indent=4)


def _features_load(path: Path):
    if not path.is_file():
        raise Exception("Can not find the file " + path)
    LOG.debug(f"Loading {path}")
    with path.open("r") as file:
        return json.load(file)


def _models_path(sample_path: str, metric: Optional[METRICS] = None) -> Path:
    return Path(
        f"{sample_path}.models" if metric is None else f"{sample_path}.model.{metric}"
    )


def _models_estimate(
    id: str,
    problem: ProblemBase,
    x: np.ndarray,
    f: np.ndarray,
    metric: METRICS,
) -> List[ModelInfo]:
    from .model import models_estimate

    if metric not in METRICS:
        raise ValueError(f"Unknown best model metric `{metric}`")
    LOG.debug(f"Finding best model of `{metric}` metric for sample {id}")
    # Note that we assume maximization problem
    models, metrics = models_estimate(problem, metric, x, -f)
    return [
        ModelInfo(
            nu=model.kernel_.nu,
            length_scale=model.kernel_.length_scale,
            metric_value=metric_value,
        )
        for model, metric_value in zip(models, metrics)
    ]


def _models_save(path: Path, models_by_metric: Dict[METRICS, List[ModelInfo]]) -> None:
    LOG.debug(f"Saving {path}")
    models_json = {}
    for metric, models in models_by_metric.items():
        models_json[metric.value] = [asdict(m) for m in models]
    with path.open("w") as file:
        json.dump(models_json, file, indent=4)


def _models_load(path: Path) -> Dict[METRICS, List[ModelInfo]]:
    if not path.is_file():
        raise Exception("Can not find the file " + path)
    LOG.debug(f"Loading {path}")
    with path.open("r") as file:
        models_json = json.load(file)
        models_by_metric = {}
        for metric, models in models_json.items():
            models_by_metric[METRICS(metric)] = [ModelInfo(**m) for m in models]
        return models_by_metric
