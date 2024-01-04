import numpy as np

from ..functions import branin
from ..problem import ProblemBase


class Problem(ProblemBase):
    def init(self):
        self.add_variable(bounds=(-5, 10), initial_guess=5)
        self.add_variable(bounds=(0, 15), initial_guess=15)
        self.add_objective()
        self.add_solution(x=[-np.pi, 12.275], f=0.3978873577)
        self.add_solution(x=[np.pi, 2.275], f=0.3978873577)
        self.add_solution(x=[9.42478, 2.475], f=0.3978873577)

    def calc_objectives(self, x):
        return [branin(*x)]
