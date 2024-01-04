import numpy as np


def factorize(dim: int, n_points: int) -> np.ndarray[int]:
    points_per_dim = int(np.ceil(np.power(n_points, 1.0 / dim)))
    return np.repeat(points_per_dim, dim)


def cells_grid(
    dim: int,
    size: int,
    random_shift: float = 0,  # value from 0 to 1 to randomly shift points within cells
) -> np.ndarray[float]:
    n_cells = factorize(dim=dim, n_points=size)
    n_points = np.product(n_cells)
    steps = [1.0 / (2.0 * n) for n in n_cells]
    # Nodes are placed at centers of cells from 0 to 1
    nodes = [np.linspace(s, 1 - s, n) for s, n in zip(steps, n_cells)]
    result = np.vstack([n.flatten() for n in np.meshgrid(*nodes)]).T
    if random_shift > 0:
        assert random_shift < 1
        bound = random_shift * np.array(steps)
        result += np.random.uniform(-bound, bound, result.shape)
    if n_points > size:
        random_idx = np.random.choice(np.arange(n_points), size, replace=False)
        result = result[random_idx]
    return result


def full_factorial(
    dim: int,
    size: int,
    randomized: bool = True,
):
    # Fills from 0 to 1 in regular grid
    n_cells = factorize(dim=dim, n_points=size)
    n_points = np.product(n_cells)
    result = np.empty((n_points, dim), dtype=float)
    repeat_count = 1
    tile_count = n_points
    for i, n_i in enumerate(n_cells):
        tile_count //= n_i
        nodes = np.random.random(n_i) if randomized else np.linspace(0, 1, n_i)
        result[:, i] = np.tile(np.repeat(nodes, repeat_count, axis=0), tile_count)
        repeat_count *= n_i
    if n_points > size:
        random_idx = np.random.choice(np.arange(n_points), size, replace=False)
        result = result[random_idx]
    return result
