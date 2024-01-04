from ..functions import fon1, fon2
from ..problem import ProblemBase, Solution


class Problem(ProblemBase):
    def __init__(self, dimension=None):
        self.dimension = dimension or 2

    def init(self):
        for _ in range(self.dimension):
            self.add_variable(bounds=(-4, 4), initial_guess=4)
        self.add_objective()
        self.add_objective()

    def calc_objectives(self, x):
        return [fon1(x), fon2(x)]
