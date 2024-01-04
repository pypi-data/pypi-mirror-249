from ..functions import perm2
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-self.__dim_x, self.__dim_x))
        self.add_objective()
        self.add_solution(x=[1.0 / (i + 1) for i in range(self.__dim_x)], f=0)

    def calc_objectives(self, x):
        return [perm2(x)]
