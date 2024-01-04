import ioh

from . import _problem


class Problem(_problem.ProblemBBOB):
    def __init__(self, dim_x=2, instance=0):
        super().__init__(
            ioh.get_problem(
                fid="Gallagher21",
                instance=instance,
                dimension=dim_x,
                problem_class=ioh.ProblemClass.BBOB,
            )
        )
