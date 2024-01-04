from ..functions import styblinskitang
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-5, 5), initial_guess=5)
        self.add_objective()
        self.add_solution(x=[-2.903534] * self.__dim_x, f=-39.1662 * self.__dim_x)

    def calc_objectives(self, x):
        return [styblinskitang(x)]
