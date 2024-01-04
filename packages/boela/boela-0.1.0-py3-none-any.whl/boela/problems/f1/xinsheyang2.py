from ..functions import xinsheyang2
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-6.28, 6.28), initial_guess=3)
        self.add_objective()
        self.add_solution(x=[0.0] * self.__dim_x, f=0.0)

    def calc_objectives(self, x):
        return [xinsheyang2(x)]
