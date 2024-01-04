from ..functions import qing
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-100, 100), initial_guess=80)
        self.add_objective()
        self.add_solution(x=[i**0.5 for i in range(1, self.__dim_x + 1)], f=0)

    def calc_objectives(self, x):
        return [qing(x)]
