from dataclasses import dataclass
from typing import List, Optional, Self, Tuple

import numpy as np

from . import vm_triples


@dataclass
class VariabilityMap:
    x: np.ndarray
    f: np.ndarray
    triples: List[Tuple[int, int, int]]
    dx_norm: Optional[np.ndarray] = None
    deltas: Optional[np.ndarray] = None
    f_stats: Optional[Tuple[float, float]] = None

    def __post_init__(self):
        if self.dx_norm is None:
            self.dx_norm = vm_triples._calc_dx_norm(self.x, self.triples)
        if self.f_stats is None:
            self.f_stats = (self.f.mean(), self.f.std())
            if self.f_stats[1] == 0:
                self.f_stats[1] = 1
        if self.deltas is None:
            f = (self.f.flatten() - self.f_stats[0]) / self.f_stats[1]
            self.deltas = np.diff(f[self.triples], axis=1) / self.dx_norm
        assert np.all(self.dx_norm > 0)

    def copy_extended(self, **kwargs) -> Self:
        x, f, triples = vm_triples.extend(self.x, self.f, self.triples, **kwargs)
        return VariabilityMap(x=x, f=f, triples=triples, f_stats=self.f_stats)

    def copy_with_model(self, model):
        return VariabilityMap(
            x=self.x,
            f=model.predict(self.x),
            triples=self.triples,
            dx_norm=self.dx_norm,
            f_stats=self.f_stats,
        )

    def validate(self, model) -> float:
        vm_model = self.copy_with_model(model)
        # TODO how we validate triples that have both 0 deltas, which means that points
        # are at constant region? Now such angles are just nan
        delta_angles = vm_triples._calc_angle_vectors(self.deltas, vm_model.deltas)
        return np.nanmean(delta_angles)

    def plot(
        self,
        scale="linear",
        fontsize=12,
        title: str = "",
        labels: np.ndarray = None,
        size: Tuple[int, int] = (8, 8),
        dpi: int = 100,
        file_name: Optional[str] = None,
    ):
        import matplotlib.pyplot as plt

        plt.figure(figsize=size, dpi=dpi)

        plt.plot(self.deltas[:, 0], self.deltas[:, 1], ".")
        if labels is not None:
            [plt.text(d0, d1, f"{l:.1f}") for (d0, d1), l in zip(self.deltas, labels)]
        plt.xlabel("$\delta_1$", fontsize=fontsize)
        plt.ylabel("$\delta_2$", fontsize=fontsize)
        plt.xscale(scale)
        plt.yscale(scale)
        x_lim = np.abs(plt.xlim()).max()
        y_lim = np.abs(plt.ylim()).max()
        plt.plot([-x_lim, x_lim], [y_lim, -y_lim], "-", c="k", alpha=0.5)
        plt.xlim([-x_lim, x_lim])
        plt.ylim([-y_lim, y_lim])
        plt.grid()
        plt.title(title)
        if file_name:
            plt.savefig(file_name)
            plt.close()
        else:
            plt.show()

    def plot_model(
        self,
        model,
        scale="linear",
        fontsize=12,
        title: str = "",
        size: Tuple[int, int] = (8, 8),
        dpi: int = 100,
        file_name: Optional[str] = None,
        model_tag: str = "",
    ):
        import matplotlib.pyplot as plt

        plt.figure(figsize=size, dpi=dpi)

        vm_model = self.copy_with_model(model)
        plt.plot(self.deltas[:, 0], self.deltas[:, 1], ".", c="k", label="sample")
        plt.plot(
            vm_model.deltas[:, 0],
            vm_model.deltas[:, 1],
            ".",
            alpha=0.7,
            markersize=2,
            label=model_tag or "model",
        )
        plt.xlabel("$\delta_1$", fontsize=fontsize)
        plt.ylabel("$\delta_2$", fontsize=fontsize)
        plt.xscale(scale)
        plt.yscale(scale)
        x_lim = np.abs(plt.xlim()).max()
        y_lim = np.abs(plt.ylim()).max()
        plt.plot([-x_lim, x_lim], [y_lim, -y_lim], "-", c="k", alpha=0.5)
        plt.xlim([-x_lim, x_lim])
        plt.ylim([-y_lim, y_lim])
        for delta, delta_step in zip(self.deltas, vm_model.deltas - self.deltas):
            plt.arrow(delta[0], delta[1], delta_step[0], delta_step[1], alpha=0.2)
        plt.legend()
        plt.grid()
        plt.title(title)
        if file_name:
            plt.savefig(file_name)
            plt.close()
        else:
            plt.show()


class Segmentation:
    def __init__(self, vm: VariabilityMap):
        self.vm = vm
        d0, d1 = vm.deltas[:, 0], vm.deltas[:, 1]
        self.angles: np.ndarray = np.angle(d0 + d1 * 1j, deg=True)
        # Make 0 angle at -45 degrees and +-180 angle at 145 degrees. That way it's
        # easier to generate sectors with respect to symmetry line of variability map.
        self.angles += 45
        self.angles[self.angles > 180] -= 360
        # Weight of triple is set by angle between its points:
        # - weight=0 if angle is 0 degrees
        # - weight=1if angle is 180 degrees
        self.weights = vm_triples._calc_angle(vm.x, vm.triples) / 180.0
        self.weights_sum = sum(self.weights)

    def _mask_sector(self, gamma: float) -> np.ndarray:
        assert 0 <= gamma <= 180
        angles_abs = np.abs(self.angles)
        return angles_abs <= gamma

    def _mask_central_sector(self, gamma: float) -> np.ndarray:
        assert 0 <= gamma <= 180
        angle_min = 90 - gamma / 2.0
        angle_max = 90 + gamma / 2.0
        angles_abs = np.abs(self.angles)
        return (angle_min <= angles_abs) * (angles_abs <= angle_max)

    def sector_ratio(self, gamma):
        mask = self._mask_sector(gamma)
        return sum(self.weights[mask]) / self.weights_sum

    def sector_ratios_grid(self, n_sectors=181):
        gammas = np.linspace(0, 180, n_sectors)
        ratios = np.zeros(gammas.size)
        for i, gamma in enumerate(gammas):
            mask = self._mask_sector(gamma)
            ratios[i] = sum(self.weights[mask])
        return gammas, ratios / self.weights_sum

    def central_sector_ratio(self, gamma):
        mask = self._mask_central_sector(gamma)
        return sum(self.weights[mask]) / self.weights_sum

    def central_sector_ratios_grid(self, n_sectors=181):
        gammas = np.linspace(0, 180, n_sectors)
        ratios = np.zeros(gammas.size)
        for i, gamma in enumerate(gammas):
            mask = self._mask_central_sector(gamma)
            ratios[i] = sum(self.weights[mask])
        return gammas, ratios / self.weights_sum

    def validate(self, model, n_sectors=19) -> float:
        sample_ratios = self.sector_ratios_grid(n_sectors)[1]
        vm_model = self.vm.copy_with_model(model)
        model_ratios = Segmentation(vm_model).sector_ratios_grid(n_sectors)[1]
        return np.nanmean(np.abs(sample_ratios - model_ratios))

    def validate_central(self, model, n_sectors=19):
        sample_ratios = self.central_sector_ratios_grid(n_sectors)[1]
        vm_model = self.vm.copy_with_model(model)
        model_ratios = Segmentation(vm_model).central_sector_ratios_grid(n_sectors)[1]
        return np.nanmean(np.abs(sample_ratios - model_ratios))

    def plot(self, model=None, n_sectors=181):
        import matplotlib.pyplot as plt

        gammas, ratios = self.sector_ratios_grid(n_sectors)
        plt.plot(gammas, ratios, label="sample")
        if model is not None:
            vm_model = self.vm.copy_with_model(model)
            vm_seg = Segmentation(vm_model)
            gammas_m, ratios_m = vm_seg.sector_ratios_grid(n_sectors)
            plt.plot(gammas_m, ratios_m, label="model")
        plt.axvline(x=0, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=45, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=90, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=135, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=180, color="k", linestyle="--", alpha=0.4)
        plt.xticks(range(0, 181, 45))
        plt.legend()
        plt.grid()
        plt.show()

    def plot_central(self, model=None, n_sectors=181):
        import matplotlib.pyplot as plt

        gammas, ratios = self.central_sector_ratios_grid(n_sectors)
        plt.plot(gammas, ratios, label="sample")
        if model is not None:
            vm_model = self.vm.copy_with_model(model)
            vm_seg = Segmentation(vm_model)
            gammas_m, ratios_m = vm_seg.central_sector_ratios_grid(n_sectors)
            plt.plot(gammas_m, ratios_m, label="model")
        plt.axvline(x=0, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=45, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=90, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=135, color="k", linestyle="--", alpha=0.4)
        plt.axvline(x=180, color="k", linestyle="--", alpha=0.4)
        plt.xticks(range(0, 181, 45))
        plt.legend()
        plt.grid()
        plt.show()


class InformationContent:
    """
    +--------+--------+--------+--------+
    |   i\j  | [=]  0 | [-] -1 | [+]  2 |
    +--------+--------+--------+--------+
    | [=]  0 |    0   |   -1   |    2   |
    +--------+--------+--------+--------+
    | [-] -1 |    1   |    0   |    3   |
    +--------+--------+--------+--------+
    | [+]  2 |   -2   |   -3   |    0   |
    +--------+--------+--------+--------+
    """

    _STEP = {"negative": -1, "neutral": 0, "positive": 2}

    def __init__(self, vm: VariabilityMap):
        self.vm = vm
        steps = list(self._STEP.values())
        self.block_types = np.array([j - i for i in steps for j in steps if i != j])
        self.ic_base = np.log(self.block_types.size)
        self.weights = vm_triples._calc_angle(vm.x, vm.triples) / 180.0
        self.weights_sum = sum(self.weights)

    def evaluate(
        self, eps1: float, eps2: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        sequence = np.zeros_like(self.vm.deltas, int)
        if eps2 is None:
            eps2 = eps1
        sequence.fill(self._STEP["neutral"])
        sequence[self.vm.deltas[:, 0] > eps1, 0] = self._STEP["positive"]
        sequence[self.vm.deltas[:, 0] < -eps2, 0] = self._STEP["negative"]
        sequence[self.vm.deltas[:, 1] > eps2, 1] = self._STEP["positive"]
        sequence[self.vm.deltas[:, 1] < -eps1, 1] = self._STEP["negative"]
        blocks = np.diff(sequence, axis=1).ravel()
        # Calculate information content
        ic = 0
        for block_type in self.block_types:
            prob = np.sum(self.weights[blocks == block_type]) / self.weights_sum
            if prob > 0:
                ic -= prob * np.log(prob) / self.ic_base
        # Ignore neutral changes, track only [+-] and [-+] blocks
        mask = blocks == (self._STEP["positive"] - self._STEP["negative"])
        mask += blocks == (self._STEP["negative"] - self._STEP["positive"])
        # Count without blocks with repeated changes
        icp = np.sum(self.weights[mask]) / (self.weights_sum + 1.0)
        return ic, icp

    def evaluate_grid_1d(
        self, eps: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if eps is None:
            eps = np.unique(np.abs(self.vm.deltas))
        ic, icp = np.vectorize(self.evaluate)(eps1=eps)
        return eps, ic.astype(float), icp.astype(float)

    def evaluate_grid_2d(
        self, eps1: Optional[float] = None, eps2: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if eps1 is None:
            eps1 = np.unique(self.vm.deltas[:, 0])
        if eps2 is None:
            eps2 = np.unique(self.vm.deltas[:, 1])
        eps = np.vstack([_.flatten() for _ in np.meshgrid(eps1, eps2)]).T
        ic, icp = np.vectorize(self.evaluate)(eps1=eps[:, 0], eps2=eps[:, 1])
        return eps, ic.reshape(-1, 1).astype(float), icp.reshape(-1, 1).astype(float)

    def validate(self, model) -> Tuple[float, float]:
        vm_model = self.vm.copy_with_model(model)
        eps, ic, icp = self.evaluate_grid_1d()
        eps, ic_m, icp_m = InformationContent(vm_model).evaluate_grid_1d(eps)
        return np.abs(ic - ic_m).mean(), np.abs(icp - icp_m).mean()

    def plot(self, model=None, eps_scale="log"):
        import matplotlib.pyplot as plt

        eps, ic, icp = self.evaluate_grid_1d()
        plt.plot(eps, ic, label="sample ic")
        plt.plot(eps, icp, label="sample icp")
        if model is not None:
            vm_model = self.vm.copy_with_model(model)
            vm_ic = InformationContent(vm_model)
            eps_m, ic_m, icp_m = vm_ic.evaluate_grid_1d()
            plt.plot(eps_m, ic_m, label="model ic")
            plt.plot(eps_m, icp_m, label="model icp")

        plt.xscale(eps_scale)
        plt.legend()
        plt.grid()
        plt.show()


def calculate(x: np.ndarray, f: np.ndarray) -> dict:
    triples = vm_triples.collect_space_filling(x, 2 * x.size, symmetric=True)
    vm = VariabilityMap(x, f, triples)
    vm_seg = Segmentation(vm)
    vm_ic = InformationContent(vm)
    deltas = np.abs(vm.deltas)
    delta_min = deltas[deltas > 0].min()  # Should not be zero for geomspace
    delta_max = deltas.max()

    features = {}

    gammas, ratios = vm_seg.sector_ratios_grid()
    idx = [30, 45, 60, 90, 120, 135, 150]
    thresh = [0.05, 0.25, 0.5, 0.75, 0.95]
    features.update({f"sector_{int(g)}": r for g, r in zip(gammas[idx], ratios[idx])})
    features.update({f"ratio_{r}": gammas[np.abs(ratios - r).argmin()] for r in thresh})

    eps_grid = np.linspace(delta_min, delta_max, 4)
    eps, ic, icp = vm_ic.evaluate_grid_1d(eps_grid)
    features.update({f"ic_{i}": ic[i] for i in range(4)})
    features.update({f"icp_{i}": icp[i] for i in range(4)})
    eps, ic, icp = vm_ic.evaluate_grid_1d()

    eps_icp_half = eps[icp < 0.5 * icp[0]]
    features.update(
        {
            "ic_max": ic.max(),
            "ic_max_eps": eps[ic.argmax()],
            "icp_init": icp[0],
            "eps_ic_s": eps[ic < 0.05][0],
            "eps_icp_half": eps_icp_half[0] if len(eps_icp_half) else np.mean(eps),
            "eps_min": eps.min(),
            "eps_max": eps.max(),
        }
    )
    eps_search = np.geomspace(delta_min, delta_max, 200)
    ic_max_eps1 = [vm_ic.evaluate_grid_2d(e, eps_search)[1].max() for e in eps_grid]
    ic_max_eps2 = [vm_ic.evaluate_grid_2d(eps_search, e)[1].max() for e in eps_grid]
    features.update({f"gic_eps1_{i}": ic_max_eps1[i] for i in range(len(eps_grid))})
    features.update({f"gic_eps2_{i}": ic_max_eps2[i] for i in range(len(eps_grid))})

    icp_max_eps1 = [vm_ic.evaluate_grid_2d(e, eps_search)[2].max() for e in eps_grid]
    icp_max_eps2 = [vm_ic.evaluate_grid_2d(eps_search, e)[2].max() for e in eps_grid]
    features.update({f"gicp_eps1_{i}": icp_max_eps1[i] for i in range(len(eps_grid))})
    features.update({f"gicp_eps2_{i}": icp_max_eps2[i] for i in range(len(eps_grid))})

    return {f"vm.{f}": v for f, v in features.items()}
