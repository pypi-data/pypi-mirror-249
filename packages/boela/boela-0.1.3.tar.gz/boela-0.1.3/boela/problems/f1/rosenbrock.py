from ..functions import rosenbrock
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-2.048, 2.048), initial_guess=-2)
        self.add_objective()
        self.add_solution(x=[1.0] * self.__dim_x, f=0)

    def calc_objectives(self, x):
        return [rosenbrock(x)]
