from typing import Set

from ..constants import PROBLEM_FEATURE, SAMPLE_FEATURE
from . import flacco, vm_features

FEATURES_FLACCO: Set = {
    SAMPLE_FEATURE.ELA_META,
    SAMPLE_FEATURE.ELA_DISTR,
    SAMPLE_FEATURE.ELA_LEVEL,
    SAMPLE_FEATURE.CM_ANGLE,
    SAMPLE_FEATURE.CM_CONV,
    SAMPLE_FEATURE.CM_GRAD,
    SAMPLE_FEATURE.CM_LIMO,
    SAMPLE_FEATURE.DISP,
    SAMPLE_FEATURE.IC,
    SAMPLE_FEATURE.NBC,
    SAMPLE_FEATURE.PCA,
    SAMPLE_FEATURE.FDC,
    PROBLEM_FEATURE.ELA_LOCAL,
    PROBLEM_FEATURE.ELA_CURV,
    PROBLEM_FEATURE.ELA_CONV,
    PROBLEM_FEATURE.LON,
    PROBLEM_FEATURE.HILL,
    PROBLEM_FEATURE.GRAD,
    PROBLEM_FEATURE.SCALE,
    PROBLEM_FEATURE.SOBOL,
}

FEATURES_VM: Set = {
    SAMPLE_FEATURE.ELA_META,
    SAMPLE_FEATURE.ELA_DISTR,
    SAMPLE_FEATURE.ELA_LEVEL,
}


def analyze_sample(feature_set: SAMPLE_FEATURE, *args, **kwargs):
    if feature_set in FEATURES_FLACCO:
        return getattr(flacco, feature_set)(*args, **kwargs)
    elif feature_set == SAMPLE_FEATURE.VARIABILITY_MAP:
        return vm_features.calculate(*args, **kwargs)
    else:
        raise ValueError(f"Unknown feature set {feature_set}")


def analyze_problem(feature_set: PROBLEM_FEATURE, *args, **kwargs):
    if feature_set in FEATURES_FLACCO:
        return getattr(flacco, feature_set)(*args, **kwargs)
    elif feature_set == SAMPLE_FEATURE.VARIABILITY_MAP:
        return vm_features.calculate(*args, **kwargs)
    else:
        raise ValueError(f"Unknown feature set {feature_set}")
