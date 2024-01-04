from ..functions import elatar
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-100, 100), initial_guess=80)
        self.add_variable(bounds=(-100, 100), initial_guess=80)
        self.add_objective()
        self.add_solution(x=[3.409186, -2.171433], f=1.7127803540)

    def calc_objectives(self, x):
        return [elatar(*x)]
