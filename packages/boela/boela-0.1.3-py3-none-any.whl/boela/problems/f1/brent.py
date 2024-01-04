from ..functions import brent
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-100, 100), initial_guess=80)
        self.add_variable(bounds=(-100, 100), initial_guess=80)
        self.add_objective()
        self.add_solution(x=[-10.0, -10.0], f=0)

    def calc_objectives(self, x):
        return [brent(*x)]
