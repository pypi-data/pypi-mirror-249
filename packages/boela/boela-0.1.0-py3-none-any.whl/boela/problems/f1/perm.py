from ..functions import perm
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-self.__dim_x, self.__dim_x))
        self.add_objective()
        self.add_solution(x=list(range(1, self.__dim_x + 1)), f=0)

    def calc_objectives(self, x):
        return [perm(x)]
