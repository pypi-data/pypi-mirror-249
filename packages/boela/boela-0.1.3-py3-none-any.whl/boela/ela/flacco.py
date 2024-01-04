import warnings

import numpy as np
from pflacco import classical_ela_features, local_optima_network_features, misc_features


# Classical ELA Features
def ela_meta(x, f):
    return classical_ela_features.calculate_ela_meta(X=x, y=f)


def ela_distr(x, f, *args, **kwargs):
    res = classical_ela_features.calculate_ela_distribution(x, f, *args, **kwargs)
    # Otherwise it fails with error on saving to json :
    # Object of type int32 is not JSON serializable
    res["ela_distr.number_of_peaks"] = float(res["ela_distr.number_of_peaks"])
    return res


def ela_level(x, f, *args, **kwargs):
    return classical_ela_features.calculate_ela_level(x, f, *args, **kwargs)


# Cell Mapping Features
def cm_angle(x, f, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_cm_angle(x, f, lb, ub, *args, **kwargs)


def cm_conv(x, f, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_cm_conv(x, f, lb, ub, *args, **kwargs)


def cm_grad(x, f, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_cm_grad(x, f, lb, ub, *args, **kwargs)


def cm_limo(x, f, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_limo(x, f, lb, ub, *args, **kwargs)


# Dispersion Features
def disp(x, f, *args, **kwargs):
    # It spams warnings for small samples:
    # - RuntimeWarning: Mean of empty slice
    # - RuntimeWarning: invalid value encountered in scalar divide
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return classical_ela_features.calculate_dispersion(x, f, *args, **kwargs)


# Information Content-Based Features
def ic(x, f, *args, **kwargs):
    try:
        return classical_ela_features.calculate_information_content(
            x, f, seed=0, *args, **kwargs
        )
    except Exception as ex:
        warnings.warn(f"Failed to calculate IC features {ex}")
        return {
            "ic.h_max": np.nan,
            "ic.eps_s": np.nan,
            "ic.eps_max": np.nan,
            "ic.eps_ratio": np.nan,
            "ic.m0": np.nan,
            "ic.costs_runtime": np.nan,
        }


# Nearest Better Features
def nbc(x, f, *args, **kwargs):
    return classical_ela_features.calculate_nbc(x, f, *args, **kwargs)


# Principal Components Features
def pca(x, f, *args, **kwargs):
    return classical_ela_features.calculate_pca(x, f, *args, **kwargs)


# Fitness Distance Correlation features
def fdc(x, f, *args, **kwargs):
    return misc_features.calculate_fitness_distance_correlation(x, f, *args, **kwargs)


# Feature sets that do require additional function evaluations
def ela_local(x, f, calc, dim, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_ela_local(
        x, f, calc, dim, lb, ub, seed=0, *args, **kwargs
    )


def ela_curv(x, f, calc, dim, lb, ub, *args, **kwargs):
    return classical_ela_features.calculate_ela_curvate(
        x, f, calc, dim, lb, ub, *args, **kwargs
    )


def ela_conv(x, f, calc, *args, **kwargs):
    return classical_ela_features.calculate_ela_conv(
        x, f, calc, seed=0, *args, **kwargs
    )


def lon(calc, dim, lb, ub, *args, **kwargs):
    nodes, edges = local_optima_network_features.compute_local_optima_network(
        calc, dim, lb, ub, seed=0, *args, **kwargs
    )
    return local_optima_network_features.calculate_lon_features(nodes, edges)


def hill(calc, dim, lb, ub, *args, **kwargs):
    return misc_features.calculate_hill_climbing_features(
        calc, dim, lb, ub, seed=0, *args, **kwargs
    )


def grad(calc, dim, lb, ub, *args, **kwargs):
    return misc_features.calculate_gradient_features(
        calc, dim, lb, ub, seed=0, *args, **kwargs
    )


def scale(calc, dim, lb, ub, *args, **kwargs):
    return misc_features.calculate_length_scales_features(
        calc, dim, lb, ub, seed=0, *args, **kwargs
    )


def sobol(calc, dim, lb, ub, *args, **kwargs):
    return misc_features.calculate_sobol_indices_features(
        calc, dim, lb, ub, seed=0, *args, **kwargs
    )
