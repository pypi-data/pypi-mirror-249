from pathlib import Path

_all = []
__all__ = [
    name.stem
    for name in Path(__file__).parent.iterdir()
    if name.suffix == ".py" and not name.stem.startswith("_")
]

for _name in __all__:
    exec(f"from . import {_name}")
    exec(f"_all.append({_name})")

# Sort by name
_all = sorted(_all, key=lambda problem: problem.Problem().NAME)
