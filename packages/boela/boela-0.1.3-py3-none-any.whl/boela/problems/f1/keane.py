from ..functions import keane
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-0.01, 10), initial_guess=10)
        self.add_variable(bounds=(-0.01, 10), initial_guess=10)
        self.add_objective()
        self.add_solution(x=[0.0, 1.39325], f=-0.6737)

    def calc_objectives(self, x):
        return [keane(*x)]
