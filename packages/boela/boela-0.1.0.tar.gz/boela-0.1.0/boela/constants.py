from enum import StrEnum
from typing import Self


class METRICS(StrEnum):
    NONE = "none"
    PREDICTED = "predicted"

    R2_CV = "R2_cv"
    SUIT_EXT = "suitability_ext"
    VM_ANGLES_EXT = "vm_angles_ext"
    SEGMENT_EXT = "segment_ext"
    SUGGESTED_F = "suggested_f"


METRICS_MAX = {
    METRICS.R2_CV,
    METRICS.SUIT_EXT,
    METRICS.SUGGESTED_F,
}
METRICS_MIN = {
    METRICS.VM_ANGLES_EXT,
    METRICS.SEGMENT_EXT,
}


class SAMPLE_FEATURE(StrEnum):
    # Sample-based features
    ELA_META = "ela_meta"
    ELA_DISTR = "ela_distr"
    ELA_LEVEL = "ela_level"
    CM_ANGLE = "cm_angle"
    CM_CONV = "cm_conv"
    CM_GRAD = "cm_grad"
    CM_LIMO = "cm_limo"
    DISP = "disp"
    IC = "ic"
    NBC = "nbc"
    PCA = "pca"
    FDC = "fdc"
    VARIABILITY_MAP = "variability_map"

    @staticmethod
    def bounds_required(feature_set: Self):
        return feature_set in {
            SAMPLE_FEATURE.CM_ANGLE,
            SAMPLE_FEATURE.CM_CONV,
            SAMPLE_FEATURE.CM_GRAD,
            SAMPLE_FEATURE.CM_LIMO,
        }


class PROBLEM_FEATURE(StrEnum):
    # Features that require additional evaluations
    ELA_LOCAL = "ela_local"
    ELA_CURV = "ela_curv"
    ELA_CONV = "ela_conv"
    LON = "lon"
    HILL = "hill"
    GRAD = "grad"
    SCALE = "scale"
    SOBOL = "sobol"

    @staticmethod
    def sample_required(feature_set: Self):
        return feature_set in {
            PROBLEM_FEATURE.ELA_LOCAL,
            PROBLEM_FEATURE.ELA_CURV,
            PROBLEM_FEATURE.ELA_CONV,
        }

    @staticmethod
    def bounds_required(feature_set: Self):
        return feature_set in {
            PROBLEM_FEATURE.ELA_LOCAL,
            PROBLEM_FEATURE.ELA_CURV,
            PROBLEM_FEATURE.LON,
            PROBLEM_FEATURE.HILL,
            PROBLEM_FEATURE.GRAD,
            PROBLEM_FEATURE.SCALE,
            PROBLEM_FEATURE.SOBOL,
        }
