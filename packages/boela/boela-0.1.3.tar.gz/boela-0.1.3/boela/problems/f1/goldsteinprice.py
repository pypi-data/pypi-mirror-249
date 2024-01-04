from ..functions import goldsteinprice
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-2, 2), initial_guess=2)
        self.add_variable(bounds=(-2, 2), initial_guess=2)
        self.add_objective()
        self.add_solution(x=[0, -1], f=3)

    def calc_objectives(self, x):
        return [goldsteinprice(*x)]
