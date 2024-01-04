from ..functions import sixhumpcamel
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-3, 3), initial_guess=3)
        self.add_variable(bounds=(-2, 2), initial_guess=2)
        self.add_objective()
        self.add_solution(x=[0.0898, -0.7126], f=-1.03164)
        self.add_solution(x=[-0.0898, 0.7126], f=-1.03164)

    def calc_objectives(self, x):
        return [sixhumpcamel(*x)]
