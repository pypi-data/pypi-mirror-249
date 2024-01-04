import time
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict, Optional, Self


@dataclass
class Timer:
    """Class to simplify time measuring routine"""

    time: Optional[int] = None
    is_running: bool = False

    def start(self) -> Self:
        if self.is_running:
            self.time = time.time() - self.time
            self.is_running = False
            print(f"WARN: timer was reset at {self.str()}")
        self.time = time.time()
        self.is_running = True
        return self

    def stop(self) -> Self:
        if not self.is_running:
            print(f"WARN: timer was not started")
            return
        self.time = time.time() - self.time
        self.is_running = False
        return self

    def str(self) -> str:
        if self.time is None:
            return f"WARN: timer was not started"
        is_tunning = ""
        time_sec = self.time
        if self.is_running:
            is_tunning = " still running"
            time_sec = time.time() - self.time
        return f"<{timedelta(seconds=time_sec)}> ({time_sec:g} sec){is_tunning}"


class set_timer:
    def __init__(self):
        self.timer = Timer()

    def __enter__(self):
        return self.timer.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.timer.stop()


@dataclass
class Timers:
    """Named timers"""

    timers: Dict[str, Timer] = field(default_factory=dict)

    def start(self, tag: str = "") -> Timer:
        self.timers.setdefault(tag, Timer()).start()
        return self.timers[tag]

    def stop(self, tag: str = "") -> Timer:
        self.timers.setdefault(tag, Timer()).stop()
        return self.timers[tag]

    def str(self, tag: Optional[str] = None) -> str:
        if tag is None:
            return {tag: timer.str() for tag, timer in self.timers.items()}
        elif tag not in self.timers:
            print(f"WARN: timer `{tag}` was not set")
            return {tag: timer.str() for tag, timer in self.timers.items()}
        else:
            return self.timers[tag].str()


timers = Timers()
