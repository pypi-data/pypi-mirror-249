from ..functions import wolfe
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(0, 2), initial_guess=2)
        self.add_variable(bounds=(0, 2), initial_guess=2)
        self.add_variable(bounds=(0, 2), initial_guess=2)
        self.add_objective()
        self.add_solution(x=[0, 0, 0], f=0)

    def calc_objectives(self, x):
        return [wolfe(*x)]
