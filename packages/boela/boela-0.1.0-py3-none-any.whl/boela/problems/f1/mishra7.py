from ..functions import mishra7
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-10, 10), initial_guess=9)
        self.add_objective()
        self.add_solution(x=[self.__dim_x**0.5] * self.__dim_x, f=0)

    def calc_objectives(self, x):
        return [mishra7(x)]
