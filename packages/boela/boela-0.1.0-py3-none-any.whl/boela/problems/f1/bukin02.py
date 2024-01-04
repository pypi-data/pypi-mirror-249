from ..functions import bukin02
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-15, -5), initial_guess=-6)
        self.add_variable(bounds=(-3, 3), initial_guess=2)
        self.add_objective()
        self.add_solution(x=[-15.0, 0.0], f=-124.75)

    def calc_objectives(self, x):
        return [bukin02(*x)]
