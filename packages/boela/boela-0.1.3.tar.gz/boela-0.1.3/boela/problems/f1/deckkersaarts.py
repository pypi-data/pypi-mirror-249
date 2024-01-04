from ..functions import deckkersaarts
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-20, 20), initial_guess=18)
        self.add_variable(bounds=(-20, 20), initial_guess=18)
        self.add_objective()
        self.add_solution(x=[0, 15], f=-24777)

    def calc_objectives(self, x):
        return [deckkersaarts(*x)]
