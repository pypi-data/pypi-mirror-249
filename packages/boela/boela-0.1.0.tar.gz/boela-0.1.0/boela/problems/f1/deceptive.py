from ..functions import deceptive
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x
        self._alpha = 0.5

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(0, 1), initial_guess=0.8)
        self.add_objective()
        self.add_solution(x=[self._alpha] * self.__dim_x, f=-1)

    def calc_objectives(self, x):
        return [deceptive(x, self._alpha)]
