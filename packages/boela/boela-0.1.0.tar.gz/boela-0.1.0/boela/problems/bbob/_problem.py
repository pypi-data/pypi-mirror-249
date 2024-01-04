import ioh

from ..problem import ProblemBase


class ProblemBBOB(ProblemBase):
    def __init__(self, ioh_problem: ioh.problem.RealSingleObjective):
        self.ioh_problem = ioh_problem

    def get_instance(self, instance):
        id = self.ioh_problem.meta_data.problem_id
        dim = self.ioh_problem.meta_data.n_variables
        problem = ProblemBBOB(ioh.get_problem(id, instance, dim))
        problem.NAME = self.NAME
        return problem

    def init(self):
        for lb, ub in zip(self.ioh_problem.bounds.lb, self.ioh_problem.bounds.ub):
            self.add_variable(bounds=(lb, ub), initial_guess=None)
        self.add_objective()
        self.add_solution(x=self.ioh_problem.optimum.x, f=self.ioh_problem.optimum.y)

    def calc_objectives(self, x):
        return [self.ioh_problem(x)]


def generate():
    from pathlib import Path

    def to_snake(name):
        return "".join(
            [
                "_" + c.lower() if i > 0 and c.isupper() else c.lower()
                for i, c in enumerate(name)
            ]
        )

    for i, name in ioh.ProblemClass.BBOB.problems.items():
        path = Path(__file__).parent / f"{to_snake(name)}.py"
        path.touch(exist_ok=True)
        print(f"Updating class {path}")
        with path.open("w") as f:
            f.write(
                f"""import ioh

from . import _problem


class Problem(_problem.ProblemBBOB):
    def __init__(self, dim_x=2, instance=0):
        super().__init__(
            ioh.get_problem(
                fid="{name}",
                instance=instance,
                dimension=dim_x,
                problem_class=ioh.ProblemClass.BBOB,
            )
        )
"""
            )
