from ..functions import gulf
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(0.1, 100), initial_guess=80)
        self.add_variable(bounds=(0.1, 100), initial_guess=80)
        self.add_variable(bounds=(0.1, 100), initial_guess=80)
        self.add_objective()
        self.add_solution(x=[50, 25, 1.5], f=0)

    def calc_objectives(self, x):
        return [gulf(*x)]
