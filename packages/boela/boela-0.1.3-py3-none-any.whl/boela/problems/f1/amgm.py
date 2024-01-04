from ..functions import amgm
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for i in range(self.__dim_x):
            self.add_variable(bounds=(0, 10), initial_guess=i % 10)
        self.add_objective()
        self.add_solution(x=[0.0] * self.__dim_x, f=0)

    def calc_objectives(self, x):
        return [amgm(x)]
