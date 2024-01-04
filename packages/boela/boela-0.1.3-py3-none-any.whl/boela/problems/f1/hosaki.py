from ..functions import hosaki
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(0, 10), initial_guess=10)
        self.add_variable(bounds=(0, 10), initial_guess=10)
        self.add_objective()
        self.add_solution(x=[4, 2], f=-2.34589)

    def calc_objectives(self, x):
        return [hosaki(*x)]
