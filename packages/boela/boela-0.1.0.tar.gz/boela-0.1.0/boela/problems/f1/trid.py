from ..functions import trid
from ..problem import ProblemBase


class Problem(ProblemBase):
    def __init__(self, dim_x=2):
        self.__dim_x = dim_x

    def init(self):
        for _ in range(self.__dim_x):
            self.add_variable(
                bounds=(-self.__dim_x**2, self.__dim_x**2),
                initial_guess=-self.__dim_x**2,
            )
        self.add_objective()
        self.add_solution(
            x=[(i + 1) * (self.__dim_x - i) for i in range(self.__dim_x)],
            f=-self.__dim_x * (self.__dim_x + 4) * (self.__dim_x - 1) / 6.0,
        )

    def calc_objectives(self, x):
        return [trid(x)]
