from ..functions import levy3
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-20, 20), initial_guess=10)
        self.add_objective()
        self.add_solution(x=[1] * self.__dim_x, f=0)

    def calc_objectives(self, x):
        return [levy3(x)]
