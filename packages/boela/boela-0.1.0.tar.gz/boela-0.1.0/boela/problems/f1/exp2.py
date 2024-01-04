from ..functions import exp2
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(0, 20), initial_guess=18)
        self.add_variable(bounds=(0, 20), initial_guess=18)
        self.add_objective()
        self.add_solution(x=[1.0, 10], f=0.0)

    def calc_objectives(self, x):
        return [exp2(*x)]
