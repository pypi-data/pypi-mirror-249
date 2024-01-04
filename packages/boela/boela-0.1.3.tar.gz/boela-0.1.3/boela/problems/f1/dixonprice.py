from ..functions import dixonprice
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(bounds=(-10, 10), initial_guess=8)
        self.add_objective()
        self.add_solution(
            x=[
                2.0 ** ((2.0 - 2.0 ** (i)) / 2.0 ** (i))
                for i in range(1, self.__dim_x + 1)
            ],
            f=0,
        )

    def calc_objectives(self, x):
        return [dixonprice(x)]
