from ..functions import himmelblau
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-6, 6), initial_guess=6)
        self.add_variable(bounds=(-6, 6), initial_guess=6)
        self.add_objective()
        self.add_solution(x=[3, 2], f=0)

    def calc_objectives(self, x):
        return [himmelblau(*x)]
