from ..functions import bukin06
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-15, -5), initial_guess=-6)
        self.add_variable(bounds=(-3, 3), initial_guess=2)
        self.add_objective()
        self.add_solution(x=[-10.0, 1.0], f=0)

    def calc_objectives(self, x):
        return [bukin06(*x)]
