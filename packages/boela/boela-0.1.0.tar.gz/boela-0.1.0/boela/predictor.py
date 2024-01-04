import logging
from pathlib import Path
from typing import Callable, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from .problems.problem import ProblemBase
from .sample import Sample

LOG = logging.getLogger(__name__)


def load_predictor(
    problem: ProblemBase,
    path: Path,
) -> Callable[[np.ndarray, np.ndarray], Tuple[float, float]]:
    predictor = joblib.load(path)

    def predict_nu(x: np.ndarray, f: np.ndarray):
        sample = Sample(id="", problem=problem, x=x, f=f)
        features_dict = sample.features()
        features = pd.DataFrame({f: [v] for f, v in features_dict.items()})
        features = features.replace([np.inf, -np.inf], np.nan)
        nu = float(predictor.predict(features)[0])
        return nu

    return predict_nu


def build_predictor(
    sample: pd.DataFrame, columns_x: List[str], column_f: str
) -> Tuple[Pipeline, dict]:
    vm_features = [_ for _ in columns_x if _.startswith("feature.vm.")]
    flacco_features = [_ for _ in columns_x if not _.startswith("feature.vm.")]
    len(columns_x), len(vm_features), len(flacco_features)

    predictor = Pipeline(
        [
            ("imputer", SimpleImputer(missing_values=np.nan, strategy="mean")),
            ("classifier", RandomForestClassifier(random_state=0, n_jobs=8)),
        ]
    )

    sample[columns_x] = sample[columns_x].replace([np.inf, -np.inf], np.nan)

    best_score = -np.inf
    best_depth = None
    for max_depth in np.arange(4, 24, 2):
        predictor.set_params(classifier__max_depth=max_depth)
        score_train, score_test = cross_validate(
            sample=sample,
            columns_x=columns_x,
            column_f=column_f,
            predictor=predictor,
        )
        LOG.debug(f"{max_depth=} {score_train=:.3f} {score_test=:.3f}")
        if score_test > best_score:
            best_score = score_test
            best_depth = max_depth

    sample_x = sample[columns_x]
    sample_f = sample[column_f]
    predictor.set_params(classifier__max_depth=best_depth)
    predictor.fit(sample_x, sample_f)
    score_train = predictor.score(sample_x, sample_f)
    LOG.info(f"  {best_depth=:<4} {best_score=:.3f} {score_train=:.3f}")
    scores = {
        "score_train": score_train,
        "score_test": np.nan,
        "score_cv": best_score,
        "depth_cv": int(best_depth),
    }
    return predictor, scores


def cross_validate(
    sample: pd.DataFrame,
    columns_x: List[str],
    column_f: str,
    predictor: Pipeline,
    cv_count: int = 5,
):
    problems_all = sample["problem"].drop_duplicates().values
    cv_scores_train = []
    cv_scores_test = []
    for problems_test in np.array_split(problems_all, cv_count, axis=0):
        masks = [sample["problem"] == p_name for p_name in problems_test]
        test_mask = np.logical_or.reduce(masks)
        train_x = sample.loc[~test_mask, columns_x]
        train_f = sample.loc[~test_mask, column_f]
        test_x = sample.loc[test_mask, columns_x]
        test_f = sample.loc[test_mask, column_f]
        predictor.fit(train_x, train_f)
        cv_scores_train.append(predictor.score(train_x, train_f))
        cv_scores_test.append(predictor.score(test_x, test_f))
    return np.mean(cv_scores_train), np.mean(cv_scores_test)
