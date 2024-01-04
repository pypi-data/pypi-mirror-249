from pathlib import Path

from ._problem import ProblemBBOB

_all = []
__all__ = [
    name.stem
    for name in Path(__file__).parent.iterdir()
    if name.suffix == ".py" and not name.stem.startswith("_")
]

for _name in __all__:
    try:
        exec(f"from . import {_name}")
        exec(f"_all.append({_name})")
    except Exception as ex:
        print(f"Failed to import {_name}: {ex}")

# Sort by name
_all = sorted(_all, key=lambda problem: problem.Problem().NAME)
