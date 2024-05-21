import time

from dowser.common.transformers import convert_to_unit
from dowser.profiler.types import CapturedTrace
from .types import TimeUnit


__all__ = ["on_call", "on_return", "on_sample"]


def get_unix_timestamp(unit: TimeUnit = "ms") -> float:
    unix_timestamp = time.time()
    return convert_to_unit(unit, "s", unix_timestamp)


def capture_trace(*_) -> CapturedTrace:
    unix_timestamp = get_unix_timestamp()

    return "unix_timestamp", int(unix_timestamp)


on_call = capture_trace
on_return = capture_trace
on_sample = capture_trace
