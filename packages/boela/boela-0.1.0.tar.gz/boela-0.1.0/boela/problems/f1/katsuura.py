from ..functions import katsuura
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(0, 1), initial_guess=1)
        self.add_objective()
        self.add_solution(x=[0.0] * self.__dim_x, f=1)

    def calc_objectives(self, x):
        return [katsuura(x)]
