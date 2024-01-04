import copy
from collections.abc import Sequence
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np

from ..constants import PROBLEM_FEATURE


def check_bounds(bounds: Sequence, name: str) -> Tuple[float, float]:
    if not isinstance(bounds, Sequence) or len(bounds) != 2:
        raise ValueError(f"Wrong bounds structure of {name}")
    bounds_float = np.array(bounds, dtype=float)
    if not np.isfinite(bounds_float[0]):
        bounds_float[0] = -np.inf
    if not np.isfinite(bounds_float[1]):
        bounds_float[1] = np.inf
    if bounds_float[0] > bounds_float[1]:
        raise ValueError(f"Invalid bound values {bounds_float.tolist()} of {name}")
    return tuple(bounds_float.tolist())


@dataclass
class Solution:
    x: np.ndarray[float]
    f: Optional[np.ndarray[float]] = None
    c: Optional[np.ndarray[float]] = None

    def __post_init__(self):
        self.x = np.atleast_1d(self.x).astype(float)
        if self.f is not None:
            self.f = np.atleast_1d(self.f).astype(float)
        if self.c is not None:
            self.c = np.atleast_1d(self.c).astype(float)

    def __str__(self):
        return (
            f"x: {np.array_str(self.x)}; "
            f"f: {np.array_str(self.f)}; "
            f"c: {np.array_str(self.c)}; "
        )


@dataclass
class Variable:
    name: str
    bounds: Tuple[float, float] = (-np.inf, np.inf)
    initial_guess: Optional[float] = None

    def __post_init__(self):
        self.bounds = check_bounds(self.bounds, str(self))
        if self.initial_guess is not None:
            self.initial_guess = float(self.initial_guess)
            if not (self.bounds[0] <= self.initial_guess <= self.bounds[1]):
                raise ValueError(f"Invalid initial guess of {self}")

    def set_initial_guess(self, initial_guess):
        if initial_guess is not None:
            self.initial_guess = float(initial_guess)
        else:
            self.initial_guess = None

    def set_bounds(self, bounds):
        self.bounds = check_bounds(bounds, str(self))

    def __str__(self) -> str:
        return f"Variable `{self.name}` in {self.bounds} {self.initial_guess}"


@dataclass
class Objective:
    name: str

    def __str__(self) -> str:
        return f"Objective `{self.name}`"


@dataclass
class Constraint:
    name: str
    bounds: Tuple[float, float] = (-np.inf, np.inf)

    def __post_init__(self):
        self.bounds = check_bounds(self.bounds, str(self))

    def set_bounds(self, bounds):
        self.bounds = check_bounds(bounds, str(self))

    def __str__(self) -> str:
        return f"Constraint `{self.name}` in {self.bounds}"


class ProblemMeta(type):
    def __call__(cls, *args, **kwargs):
        problem: ProblemBase = type.__call__(cls, *args, **kwargs)  # overwritten
        problem._initialize()  # fixed method
        problem.init()  # overwritten
        # Number of variables is available after prepare problem
        problem.step = [0] * problem.dim_x
        problem.shift = [0] * problem.dim_x
        problem.rotation["matrix"] = [[np.nan] * problem.dim_x] * problem.dim_x
        return problem


class ProblemBase(metaclass=ProblemMeta):
    def _initialize(self):
        self.NAME: str = self.__module__.replace("boela.problems.", "")

        self.calls_count = 0
        self.variables: List[Variable] = []
        self.objectives: List[Objective] = []
        self.constraints: List[Constraint] = []
        self.solutions: List[Solution] = []
        self._history_cache: List[List[float]] = []

        self.scale = (0, 1)
        self.noise = 0
        self.step = []
        self.shift = []
        self.rotation = {"angle": 0, "matrix": [[]]}

    @property
    def id(self):
        return f"{self.NAME}_{self.dim_x}"

    # USER SIDE METHODS

    def init(self):
        raise Exception("Problem was not initialized")

    def calc_objectives(self, x):
        raise Exception("Objectives was not defined")

    def calc_constraints(self, x):
        raise Exception("Constraints was not defined")

    # EVALUATION METHODS

    def _calc_f(self, x):
        return np.array([self.calc_objectives(xi) for xi in x])

    def _calc_c(self, x):
        return np.array([self.calc_constraints(xi) for xi in x])

    def print_iters(self, step=1):
        self.i_print = lambda n, i: [
            print(_, end="'") for _ in range(n + 1, n + i + 1) if _ % step == 0
        ]
        return self

    def calc(self, x):
        x = np.atleast_2d(x)
        if x.shape[1] != self.dim_x:
            raise Exception("Wrong dimension of input points: " + str(x))

        batch_size = x.shape[0]
        designs = np.zeros((batch_size, self.dim_xfc))
        designs[:, : self.dim_x] = x
        if self.dim_f > 0:
            designs[:, self.dim_x : self.dim_x + self.dim_f] = self._calc_f(x)
        if self.dim_c > 0:
            designs[:, self.dim_x + self.dim_f :] = self._calc_c(x)

        getattr(self, "i_print", lambda *_: _)(self.calls_count, batch_size)

        self.calls_count += batch_size
        self._history_cache.extend(designs.tolist())
        return designs[:, self.dim_x :]

    # ADD METHODS

    def add_variable(self, bounds, initial_guess=None, name=None):
        assert not self.solutions, "Solutions can not be added before the variables"
        if not name:
            name = f"x[{self.dim_x + 1}]"
        self.variables.append(Variable(name, bounds, initial_guess))

    def add_objective(self, name=None):
        assert not self.solutions, "Solutions can not be added before the objectives"
        if not name:
            name = f"f[{self.dim_f + 1}]"
        self.objectives.append(Objective(name))

    def add_constraint(self, bounds, name=None):
        assert not self.solutions, "Solutions can not be added before the constraints"
        if not name:
            name = f"c[{self.dim_c + 1}]"
        self.constraints.append(Constraint(name, bounds))

    def add_solution(
        self,
        x: Sequence,
        f: Optional[Sequence] = None,
        c: Optional[Sequence] = None,
    ):
        x = np.atleast_1d(x)
        assert len(x) == self.dim_x
        if f is not None:
            f = np.atleast_1d(f)
            assert len(f) == self.dim_f
        if c is not None:
            c = np.atleast_1d(c)
            assert len(c) == self.dim_c
        self.solutions.append(Solution(x=x, f=f, c=c))
        if self.dim_f == 1 and len(self.solutions) > 1:
            f_values = [_.f[0] for _ in self.solutions]
            assert np.all(f_values[0] == f_values)

    # SIZE METHODS

    @property
    def dim_x(self):
        return len(self.variables)

    @property
    def dim_f(self):
        return len(self.objectives)

    @property
    def dim_c(self):
        return len(self.constraints)

    @property
    def dim_fc(self):
        return self.dim_f + self.dim_c

    @property
    def dim_xfc(self):
        return self.dim_x + self.dim_f + self.dim_c

    # NAMES METHODS

    @property
    def variable_names(self):
        return [_.name for _ in self.variables]

    @property
    def constraint_names(self):
        return [_.name for _ in self.constraints]

    @property
    def objective_names(self):
        return [_.name for _ in self.objectives]

    # BOUNDS AND INITIAL GUESS METHODS

    @property
    def variable_bounds(self):
        return list(zip(*[_.bounds for _ in self.variables]))

    @property
    def constraint_bounds(self):
        return list(zip(*[_.bounds for _ in self.constraints]))

    @property
    def initial_guess(self):
        return [_.initial_guess for _ in self.variables]

    # HISTORY METHODS

    @property
    def history(self):
        return np.array(self._history_cache)

    def clear_history(self):
        self._history_cache = []
        self.calls_count = 0

    def modify(
        self,
        noise: float = 0,
        step=0,
        scale=(0, 1),
        shift=0,
        rotation=0,
        seed=None,
    ):
        problem = copy.deepcopy(self)
        problem.clear_history()

        # Modify objective function
        define_objectives = problem.calc_objectives

        # Add noise to objective function
        if noise != 0:
            assert noise > 0
            problem.noise = noise

            def noise_wrapper(function):
                def wrapped(x):
                    result = np.array(function(x))
                    return result * np.random.uniform(1, 1 + noise)

                return wrapped

            define_objectives = noise_wrapper(define_objectives)

        # Shift objective function
        if shift != 0:
            assert shift > 0
            if np.ndim(shift) == 0:
                if seed is not None:
                    np.random.seed(seed)
                # x_domain = np.diff(problem.variables_bounds, axis=0).ravel()
                # shift = np.random.uniform(low=-shift * x_domain, high=shift * x_domain, size=problem.size_x)
                direction = np.random.choice((-1, 1), problem.dim_x)
                max_steps = np.diff(problem.variable_bounds, axis=0)[0]
                shift = shift * max_steps * direction
            elif np.ndim(shift) > 1:
                shift = np.array(shift).flatten()
            assert len(shift) == self.dim_x, f"Wrong shape of shift"

            problem.shift = shift

            def shift_wrapper(function):
                return lambda x: function(x + shift)

            define_objectives = shift_wrapper(define_objectives)

        # Rotate objective function
        if rotation != 0:
            if isinstance(rotation, dict):
                if "angle" not in rotation or "matrix" not in rotation:
                    raise AttributeError("Wrong value of rotation.")
                if np.array(rotation["matrix"]).shape != (
                    problem.dim_x,
                    problem.dim_x,
                ):
                    raise AttributeError("Wrong value of rotation matrix.")
                problem.rotation = rotation
            elif np.array(rotation).ndim == 0:
                if seed is not None:
                    np.random.seed(seed)
                # Vectors of the rotation plane
                v1 = np.random.rand(problem.dim_x)
                v2 = np.random.rand(problem.dim_x)
                # Gram-Schmidt orthogonalization
                n1 = v1 / np.linalg.norm(v1)
                v2 = v2 - np.dot(n1, v2) * n1
                n2 = v2 / np.linalg.norm(v2)
                # Rotation matrix preparation
                # Normalize angle since the area out of domain depends on dimensionality
                angle = rotation / problem.dim_x
                identity = np.identity(problem.dim_x)
                generator2 = (np.outer(n2, n1) - np.outer(n1, n2)) * np.sin(angle)
                generator3 = (np.outer(n1, n1) + np.outer(n2, n2)) * (np.cos(angle) - 1)
                rot_matrix = identity + generator2 + generator3
                problem.rotation = {"angle": angle, "matrix": rot_matrix.tolist()}

            x_center = np.mean(problem.variable_bounds, axis=0)

            def rotation_wrapper(function):
                return lambda x: function(
                    np.dot(x - x_center / 2.0, problem.rotation["matrix"])
                    + x_center / 2.0
                )

            define_objectives = rotation_wrapper(define_objectives)

        # Scale objective function to mean 0 and std 1 (if current scale differs)
        if scale != (0, 1):
            problem.scale = scale

            def scale_wrapper(function):
                return lambda x: np.array(function(x) - scale[0]) / scale[1]

            define_objectives = scale_wrapper(define_objectives)

        # Set step for problem inputs
        if isinstance(step, (list, tuple, np.ndarray)):
            assert (
                len(step) == problem.dim_x
            ), "Resolution should be an array of length size_x or double"
        else:
            step = [step] * problem.dim_x
        if np.any(np.array(step) > 0):
            problem.step = step

            def step_wrapper(function):
                def stepped_function(x):
                    for i, res in enumerate(problem.step):
                        x[i] = res * np.round(x[i] / res) if res > 0 else x[i]
                    return function(x)

                return stepped_function

            define_objectives = step_wrapper(define_objectives)

        problem.calc_objectives = define_objectives
        return problem

    def sample_ff(self, size, seed=None, random=True):
        from . import doe

        if seed is not None:
            np.random.seed(seed)
        lb, ub = np.array(self.variable_bounds)
        x = lb + doe.full_factorial(self.dim_x, size, random) * (ub - lb)
        return x, self.calc(x)

    def sample_grid(self, size, seed=None, random_shift=0, partial=False):
        from . import doe

        if seed is not None:
            np.random.seed(seed)
        lb, ub = np.array(self.variable_bounds)
        x = lb + doe.cells_grid(self.dim_x, size, random_shift) * (ub - lb)
        if partial and size is not None and size < len(x):
            x = x[np.random.choice(np.arange(len(x)), size, replace=False)]
        return x, self.calc(x)

    def sample_rand(self, size, seed=None):
        if seed is not None:
            np.random.seed(seed)
        lb, ub = np.array(self.variable_bounds)
        x = lb + np.random.rand(size, self.dim_x) * (ub - lb)
        return x, self.calc(x)

    def sample_lhs(self, size, seed=None, centered=False):
        from scipy.stats import qmc

        sampler = qmc.LatinHypercube(d=self.dim_x, seed=seed, centered=centered)
        x = qmc.scale(sampler.random(size), *self.variable_bounds)
        return x, self.calc(x)

    def features(self, feature: PROBLEM_FEATURE, *args, x=None, f=None, **kwargs):
        from ..ela import analyze_problem

        if feature not in PROBLEM_FEATURE:
            raise ValueError(f"Features of type {feature} require sample")
        sample_required = PROBLEM_FEATURE.sample_required(feature)
        bounds_required = PROBLEM_FEATURE.bounds_required(feature)
        if sample_required and (x is None or f is None):
            raise ValueError(f"Sample is required for `{feature}` features")
        lb, ub = self.variable_bounds
        # Flacco for list bound and fail with tuples
        lb, ub = list(lb), list(ub)
        calc = self.calc_objectives
        if sample_required and bounds_required:
            return analyze_problem(
                feature, x, f, calc, self.dim_x, lb, ub, *args, **kwargs
            )
        elif sample_required and not bounds_required:
            return analyze_problem(feature, x, f, calc, *args, **kwargs)
        elif not sample_required and bounds_required:
            return analyze_problem(feature, calc, self.dim_x, lb, ub, *args, **kwargs)
        else:
            return analyze_problem(feature, calc, self.dim_x, *args, **kwargs)

    def plot(
        self,
        n_nodes_x1=50,
        n_nodes_x2=50,
        n_nodes_f=50,
        contour=False,
        wireframe=False,
        sample_x: np.ndarray = None,
        sample_f: np.ndarray = None,
        size=(6, 5),
        file_name=None,
        dpi=100,
    ):
        from ..model import plot_surface

        if self.dim_x != 2:
            raise Exception("For 2d problems only!")
        plot_surface(
            func=self.calc,
            lower_bound=self.variable_bounds[0],
            upper_bound=self.variable_bounds[1],
            n_nodes_x1=n_nodes_x1,
            n_nodes_x2=n_nodes_x2,
            n_nodes_f=n_nodes_f,
            contour=contour,
            sample_x=sample_x,
            sample_f=sample_f,
            wireframe=wireframe,
            file_name=file_name,
            title=self.NAME,
            size=size,
            dpi=dpi,
        )
