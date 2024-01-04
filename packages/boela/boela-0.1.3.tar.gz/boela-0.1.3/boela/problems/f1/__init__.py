import inspect
from pathlib import Path

_all = []
_classes = set([])
__all__ = [
    name.stem
    for name in Path(__file__).parent.iterdir()
    if name.suffix == ".py" and not name.stem.startswith("_")
]


def add_problem(class_name: str, func_name: str):
    if class_name in globals():
        return f"{class_name}.append({func_name})"
    else:
        _classes.add(class_name)
        return f"{class_name} = [{func_name}]"


for _name in __all__:
    exec(f"from . import {_name}")
    exec(f"_all.append({_name})")
    # Classify problem by multi-modality (_u, _m, _x)
    exec(f"from ..functions import {_name} as _function")
    exec(add_problem(class_name=f"_t{_function.func_type}", func_name=_name))
    # Classify problem by dimension (_d2, _d3, ..., _dn)
    args = [arg for arg in inspect.getfullargspec(_function).args if "x" in arg]
    if ["x"] == args:
        exec(add_problem(class_name="_dn", func_name=_name))
    else:
        exec(add_problem(class_name=f"_d{len(args)}", func_name=_name))

# Sort by name
_all = sorted(_all, key=lambda problem: problem.Problem().NAME)
for class_name in _classes:
    exec(f"{class_name}.sort(key=lambda problem: problem.Problem().NAME)")

# Check that all problems were classified
assert len(__all__) == sum(eval(f"len({c})") for c in _classes if c.startswith("_d"))
assert len(__all__) == sum(eval(f"len({c})") for c in _classes if c.startswith("_t"))
