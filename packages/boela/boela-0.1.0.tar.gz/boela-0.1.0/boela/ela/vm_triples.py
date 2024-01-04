import itertools
import logging
from typing import Dict, List, Optional, Set, Tuple

import numpy as np

PRECISION = 12
LOG = logging.getLogger(__name__)


def _normalize_x(x: np.ndarray) -> np.ndarray:
    # Normalize values along dimensions
    x = np.array(x, copy=True)
    for i in np.arange(x.shape[1]):
        x[:, i] = (x[:, i] - x[:, i].mean()) / x[:, i].std(ddof=1)
    return x


def _normalize_distances(distances):
    n = len(distances)
    distances_triu = distances[np.triu_indices(n, k=1)]
    distances_triu_idx = np.argsort(distances_triu)
    min_dist = distances_triu.min()
    max_dist = distances_triu.max()
    distances_triu_normed = np.linspace(min_dist, max_dist, len(distances_triu))
    distances_triu_normed = distances_triu_normed[np.argsort(distances_triu_idx)]
    distances_normed = np.zeros_like(distances)
    distances_normed[np.triu_indices(n, k=1)] = distances_triu_normed
    distances_normed += distances_normed.T
    return distances_normed


def _calc_angle_vectors(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    assert v1.shape == v2.shape
    # dot product for each row
    dot = np.einsum("ij, ij->i", v1, v2)
    norm = np.linalg.norm(v1, axis=1) * np.linalg.norm(v2, axis=1)
    # May be nan for zero-length vectors
    norm[norm == 0] = np.nan
    cosine_angle = np.round(dot / norm, PRECISION)
    angle = np.arccos(cosine_angle)
    np.degrees(angle, out=angle)
    return angle


def _calc_angle(x: np.ndarray, triples: List[Tuple[int, int, int]]) -> np.ndarray:
    v1 = x[triples[:, 0]] - x[triples[:, 1]]
    v2 = x[triples[:, 2]] - x[triples[:, 1]]
    return _calc_angle_vectors(v1, v2)


def _calc_dx_norm(x: np.ndarray, triples: List[Tuple[int, int, int]]) -> np.ndarray:
    dx_norm = np.hypot.reduce(np.diff(x[triples], axis=1), axis=2)
    np.round(dx_norm, PRECISION, out=dx_norm)
    return dx_norm


def _calc_std_mean(
    x: np.ndarray,
    f: np.ndarray,
    n_points: int = 10_000,
) -> float:
    from ..model import build_gp_matern

    np.random.seed(0)
    x_sample = np.random.uniform(x.min(0), x.max(0), size=(n_points, x.shape[1]))
    std_means = []
    for ls in np.logspace(-5, 5, 11):
        model = build_gp_matern(x=x, f=f, length_scale=ls, length_scale_bounds="fixed")
        std_means.append(model.predict(x_sample, return_std=True)[1].mean())
    return np.mean(std_means)


def _calc_std_max(
    x: np.ndarray,
    f: np.ndarray,
    n_restarts: int = 100,
) -> float:
    from scipy import optimize

    from ..model import build_gp_matern

    model = build_gp_matern(x=x, f=f, n_restarts_optimizer=5)

    def std(model, x):
        x = np.atleast_2d(x)
        _, std_pred = model.predict(x, return_std=True)
        return std_pred

    x_min = x.min(0)
    x_max = x.max(0)
    np.random.seed(0)
    x_inits = np.random.uniform(x_min, x_max, size=(n_restarts, x.shape[1]))
    best_x, best_f = None, np.inf
    for x_init in x_inits:
        res = optimize.minimize(
            lambda _: -std(model, _),
            x_init,
            bounds=list(zip(x_min, x_max)),
            method="L-BFGS-B",
        )
        if res.success and res.fun < best_f:
            best_f = res.fun
            best_x = res.x
    return best_x, -best_f


def plot(
    x: np.ndarray,
    triples: List[Tuple[int, int, int]],
    f: np.ndarray = None,
    title: str = "",
    size: Tuple[int, int] = (10, 6),
    dpi: int = 100,
    file_name: Optional[str] = None,
):
    import matplotlib.pyplot as plt

    plt.figure(figsize=size, dpi=dpi)

    [plt.plot(xt[:, 0], xt[:, 1]) for xt in x[triples]]
    plt.plot(x[:, 0], x[:, 1], ".", c="k")
    if f is not None:
        [
            plt.text(xi[0], xi[1], f"{i}|{fi[0]:.1f}", fontsize=8)
            for i, (xi, fi) in enumerate(zip(x, f))
        ]
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    plt.title(title)
    plt.grid()
    if file_name:
        plt.savefig(file_name)
        plt.close()
    else:
        plt.show()


def collect_fixed_step(
    x: np.ndarray,
    max_step: float = 1.1,
    min_angle_deg: int = 90,
    symmetric: bool = False,
    normalize_distances: bool = True,
) -> List[Tuple[int, int, int]]:
    """
    - Iterative search algorithm
    - The number of triples is fixed and depends on parameters set (may be extreme in higher dimensions)
    - Generates triples with worse angle in average (less than 180)
    - Generates triples with better distances in average (points are closer to each other)
    - Nice for small samples at moderate dimensions
    """
    assert 0 <= max_step
    assert 0 <= min_angle_deg <= 180

    x = _normalize_x(x)
    # Calculate max min distance to determine step size
    distances = np.hypot.reduce(x[:, np.newaxis] - x, axis=2)
    if normalize_distances:
        distances = _normalize_distances(distances)
    np.round(distances, PRECISION, out=distances)
    # Remove duplicates
    distances[distances < np.finfo(float).eps] = np.inf
    max_min_distance = distances.min(0).max()
    step_size = max_min_distance * max_step

    # Find triples of points
    n = x.shape[0]
    triples: List[Tuple[int, int, int]] = []
    for i in np.arange(n):
        closest_idx = np.argwhere(distances[i] <= step_size).flatten()
        if closest_idx.size < 2:
            continue
        candidate_triples = []
        for i1, i3 in itertools.combinations(closest_idx, 2):
            candidate_triples.append((i1, i, i3))
        candidate_triples = np.array(candidate_triples)
        angles = _calc_angle(x, candidate_triples)
        triples.extend(candidate_triples[angles >= min_angle_deg])
    triples = np.array(triples)
    if symmetric:
        triples = np.vstack((triples, triples[:, [2, 1, 0]]))
    return triples


def collect_random(
    x: np.ndarray,
    n_triples: int,
    max_step: float = 1.0,
    step_multiplier: float = 1.2,
    min_angle_deg: int = 90,
    seed: int = 0,
    symmetric: bool = False,
):
    """
    - Iterative search algorithm
    - Can generate the specified number of triples
    - Generates triples with better angle in average (closer to 180)
    - Generates triples with worse distances in average (points are more distant)
    - Nice for huge samples at higher dimensions when the required number of fronts is known
    """
    assert 0 <= max_step
    np.random.seed(seed)

    x = _normalize_x(x)
    # Calculate max min distance to determine step size
    distances = np.hypot.reduce(x[:, np.newaxis] - x, axis=2)
    np.round(distances, PRECISION, out=distances)
    # Remove duplicates
    distances[distances < np.finfo(float).eps] = np.inf
    max_min_distance = distances.min(0).max()
    step_size = max_min_distance * max_step

    def _iterate_randomly(n_values):
        n = 0
        while True:
            has_neighbors_mask = np.sum(np.isfinite(distances), axis=1) > 1
            indices = np.arange(n_values)[has_neighbors_mask]
            np.random.shuffle(indices)
            if indices.size == 0:
                break
            for i in indices:
                n += 1  # should start from 1
                yield i, n

    # Set this parameter to 1 to select triples with best angles, but it may slow down
    # the algorithm and increase distances between the points of triples
    triples_per_point = int(np.clip(n_triples / x.shape[0], 1, np.inf)) + 1

    triples: Set[Tuple[int, int, int]] = set()
    random_idx = _iterate_randomly(x.shape[0])
    check_point = int(10 * max(x.shape[0], n_triples))
    while len(triples) < n_triples:
        # Select next point randomly and find neighbors
        try:
            i2, n = next(random_idx)
        except StopIteration:
            LOG.debug(
                f"WARN: {n_triples} triples requested but only {len(triples)} "
                f"collected, sample size {len(x)} is not enough"
            )
            break
        neighbors = np.argwhere(distances[i2] <= step_size).flatten()
        if neighbors.size > 1:
            # Form candidate triples starting from a random point
            candidate_triples = []
            for i1, i3 in itertools.combinations(neighbors, 2):
                candidate_triples.append((i1, i2, i3))
            candidate_triples = np.array(candidate_triples)
            # Choose fronts having maximum angle assumed by its points
            angles = _calc_angle(x, candidate_triples)
            sorted_idx = (-angles).argsort()
            for i in sorted_idx[:triples_per_point]:
                i1, i2, i3 = candidate_triples[i]
                # Do not select these 2 points next time e.g. in case if angle is less than required
                distances[i2, [i1, i3]] = np.inf
                if angles[i] < min_angle_deg:
                    break
                # Increase distances to reduce "weight" of that points next time
                distances[i1, i2] *= step_multiplier
                distances[i3, i2] *= step_multiplier
                triples.add((i1, i2, i3))
                if len(triples) == n_triples:
                    break
        # Increase step_size to avoid infinite loops
        if n % check_point == 0:
            step_size *= step_multiplier
    triples = np.array(list(triples))
    if symmetric:
        triples = np.vstack((triples, triples[:, [2, 1, 0]]))
    return triples


def collect_space_filling(
    x: np.ndarray,
    n_triples: int,
    min_angle_deg: int = 90,
    n_angle_ranges: int = 3,
    step_multiplier: float = 1.1,
    seed: int = 0,
    shuffle: bool = True,
    symmetric: bool = False,
):
    """
    Increasing step multiplier increases number of unique pairs but also increases the
    average distance between paired points.
    """
    assert (
        step_multiplier > 1
    ), "Step multiplier must be more than 1 to avoid infinite looping"
    np.random.seed(seed)

    x = _normalize_x(x)
    # Calculate max min distance to determine step size
    distances = np.hypot.reduce(x[:, np.newaxis] - x, axis=2)
    np.round(distances, PRECISION, out=distances)
    # Remove duplicates
    distances[distances < np.finfo(float).eps] = np.inf
    mean_distances = np.nanmean(np.nan_to_num(distances, posinf=np.nan), axis=1)

    def _iterate_randomly(n_values):
        indices = np.arange(n_values)
        if shuffle:
            np.random.shuffle(indices)
        while True:
            for i in indices:
                yield i

    angle_ranges = np.linspace(min_angle_deg, 180, n_angle_ranges + 1)
    angle_ranges = np.vstack([angle_ranges[:-1], angle_ranges[1:]]).T
    angle_ranges[-1, -1] += 1  # For strict inequality check

    n = x.shape[0]
    random_idx = _iterate_randomly(n)
    triples: List[Tuple[int, int, int]] = []

    while len(triples) < n_triples:
        # Select next point randomly and find the closest point
        i2 = next(random_idx)
        if not np.isfinite(distances[i2]).any():
            LOG.debug(
                f"WARN: {n_triples} triples requested but only {len(triples)} "
                f"collected, sample size {n} is not enough"
            )
            break
        i1 = np.argmin(distances[i2])
        distances[i2, i1] = np.inf
        # Build candidate triples from 2 closest points and all other points

        i3_list = np.delete(np.arange(n), [i2, i1])
        less_than_mean_distance = distances[i2, i3_list] <= mean_distances[i2]
        i3_list = i3_list[np.argwhere(less_than_mean_distance).flatten()]
        i2_list = np.tile(i2, len(i3_list))
        i1_list = np.tile(i1, len(i3_list))
        candidate_triples = np.vstack([i1_list, i2_list, i3_list]).T
        # Calculate angles to select the closest point within each angle range
        angles = _calc_angle(x, candidate_triples)
        for a_min, a_max in angle_ranges:
            best_idx = np.argwhere((a_min <= angles) * (angles < a_max)).flatten()
            # Point indices that satisfy the current angle range
            best_idx = candidate_triples[best_idx][:, -1]
            best_distances = distances[i2, best_idx]
            if not np.isfinite(best_distances).any():
                # Also checks for zero size of best_distances
                continue
            # Select the closest point in that angle range
            i3 = best_idx[best_distances.argmin()]
            triples.append((i1, i2, i3))
            # Increase distances so we do not choose the same points next time
            distances[i2, i3] *= step_multiplier
            if len(triples) == n_triples:
                break
    triples = np.array(triples)
    assert len(triples) == len(np.unique(triples, axis=0))
    if triples.size and symmetric:
        triples = np.vstack((triples, triples[:, [2, 1, 0]]))
    return triples


def extend(
    x: np.ndarray[float],
    f: np.ndarray[float],
    triples: np.ndarray[int],  # matrix of shape (n_triples, 3)
    n_splits_min: int = 1,
    n_splits_max: int = 3,
    n_splits_adaptive: bool = True,
    log_splits: bool = True,
    log_rate: float = 10.0,
    symmetric: bool = False,
) -> Tuple[np.ndarray[float], np.ndarray[float], np.ndarray[int]]:
    assert n_splits_max >= n_splits_min > 0

    # Pairs of step sizes for each triple - matrix of shape (n_triples, 2)
    dx_norm = _calc_dx_norm(x, triples)
    # Merge all triples into single 1D partially linear curve, such way we interpolate
    # all the new points in one call of np.interp
    zero_steps = np.zeros((len(dx_norm), 1))
    x_path_1D = np.cumsum(np.hstack([zero_steps, dx_norm]))
    f_path_1D = f[triples].flatten()

    # Estimate number of splits for each step depending on step size
    if n_splits_adaptive:
        min_step = dx_norm.min() / (n_splits_min + 1)
        max_step = dx_norm.max() / (n_splits_max + 1)
        mean_step = np.mean([min_step, max_step])
        n_ranges = np.floor(dx_norm / mean_step).astype(int)
        n_splits = np.clip(n_ranges - 1, n_splits_min, n_splits_max)
    else:
        n_splits_list = np.arange(n_splits_min, n_splits_max + 1)
        dx_ranges = np.linspace(dx_norm.min(), dx_norm.max(), len(n_splits_list) + 1)
        n_splits = np.empty_like(dx_norm, dtype=int)
        n_splits[:, 0] = np.argmax(dx_norm[:, [0]] <= dx_ranges, axis=1)
        n_splits[:, 1] = np.argmax(dx_norm[:, [1]] <= dx_ranges, axis=1)
        np.clip(n_splits - 1, 0, len(n_splits_list) - 1, out=n_splits)
        n_splits = n_splits_list[n_splits]

    weights: Dict[int, np.ndarray] = {}
    for i in np.unique(n_splits):
        w = np.linspace(0, 1, i + 2)[1:-1]
        if log_splits:
            w = 1.0 / (1.0 + np.exp(-log_rate * (w - 0.5)))
        weights[i] = np.vstack([w[::-1], w]).T

    triples_new = []
    x_new_1D = []
    x_new = []
    # Here we map ranges of triples to indices of new points generated within that
    # range. Multiple triples may share the same range, so we do not generate duplicated
    # points within such ranges and reuse the existing indices.
    new_idx_map = {}

    # Variable to increment new points indices
    i_new = x.shape[0]
    for i, ((t1, t2, t3), (n1, n2)) in enumerate(zip(triples, n_splits)):
        # Nodes of 1D partially linear curve corresponding to i-th triple
        x1_1D, x2_1D, x3_1D = x_path_1D[i * 3 : (i + 1) * 3]

        # Unique id of the 1st range from sorted indices of the first 2 points
        range1_id = (t1, t2) if t1 <= t2 else (t2, t1)
        # But first check if new points have not already been generated in that range.
        if range1_id not in new_idx_map:
            # Interpolate along the range in original x space to generate new points.
            # In linear case it's just np.linspace(x[t1], x[t2], 2 + n1)[1:-1]
            x_interp = weights[n1] @ x[[t1, t2]]
            x_new.extend(x_interp)

            # Interpolate along the range for 1D partially linear curve
            # In linear case it's just np.linspace(x1_1D, x2_1D, 2 + n1)[1:-1]
            x_interp_1D = weights[n1] @ [x1_1D, x2_1D]
            x_new_1D.extend(x_interp_1D)
            # Cache indices of newly generated points
            new_idx_map[range1_id] = list(range(i_new, i_new + n1))
            i_new += n1

        # Unique id of the 2nd range from sorted indices of the second 2 points
        range2_id = (t2, t3) if t2 <= t3 else (t3, t2)
        # But first check if new points have not already been generated in that range.
        if range2_id not in new_idx_map:
            # Interpolate along the range in original x space to generate new points.
            # In linear case it's just np.linspace(x[t2], x[t3], 2 + n2)[1:-1]
            x_interp = weights[n2] @ x[[t2, t3]]
            x_new.extend(x_interp)
            # Interpolate along the range for 1D partially linear curve
            # In linear case it's just np.linspace(x2_1D, x3_1D, 2 + n2)[1:-1]
            x_interp_1D = weights[n2] @ [x2_1D, x3_1D]
            x_new_1D.extend(x_interp_1D)
            # Cache indices of newly generated points
            new_idx_map[range2_id] = list(range(i_new, i_new + n2))
            i_new += n2

        path = [t1, *new_idx_map[range1_id], t2, *new_idx_map[range2_id], t3]
        # Add all possible triples along that path, triples may be duplicated
        # for some ranges but we will filter them out later since they are going to
        # have the same indices of newly generated points.
        triples_new.extend(np.vstack([path[:-2], path[1:-1], path[2:]]).T)

    f_new = np.interp(x_new_1D, x_path_1D, f_path_1D).reshape(-1, 1)

    triples_new = np.unique(triples_new, axis=0)
    if symmetric:
        triples_new = np.vstack((triples_new, triples_new[:, [2, 1, 0]]))

    x_ext = np.vstack([x, x_new])
    f_ext = np.vstack([f, f_new])
    triples_ext = np.vstack([triples, triples_new])
    return x_ext, f_ext, triples_ext
