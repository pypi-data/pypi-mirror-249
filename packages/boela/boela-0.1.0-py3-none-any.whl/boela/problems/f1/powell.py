from ..functions import powell
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=4):
        self.__dim_x = dim_x
        if self.__dim_x % 4 != 0:
            raise ValueError("The problem dim_x should be multiple of 4")

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-4, 5), initial_guess=4)
        self.add_objective()
        self.add_solution(x=[0.0] * self.__dim_x, f=0)

    def calc_objectives(self, x):
        return [powell(x)]
