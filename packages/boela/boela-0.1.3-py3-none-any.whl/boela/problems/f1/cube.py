from ..functions import cube
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-10, 10), initial_guess=8)
        self.add_variable(bounds=(-10, 10), initial_guess=8)
        self.add_objective()
        self.add_solution(x=[1.0] * 2, f=0)

    def calc_objectives(self, x):
        return [cube(*x)]
