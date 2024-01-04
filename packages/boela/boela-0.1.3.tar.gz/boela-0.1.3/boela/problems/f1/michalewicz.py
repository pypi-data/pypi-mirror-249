from ..functions import michalewicz
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(0, 3.1415))
        self.add_objective()

    def calc_objectives(self, x):
        return [michalewicz(x)]
