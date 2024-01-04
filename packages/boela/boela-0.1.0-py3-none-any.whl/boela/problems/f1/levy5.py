from ..functions import levy5
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-2, 2), initial_guess=1)
        self.add_variable(bounds=(-2, 2), initial_guess=1)
        self.add_objective()
        self.add_solution(x=[-1.3086, -1.4248], f=-176.1376)

    def calc_objectives(self, x):
        return [levy5(*x)]
