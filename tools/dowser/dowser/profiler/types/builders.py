from typing import Callable
from toolz import compose, identity
from dowser.logger import get_logger
from dowser.profiler.context import profiler_context
from .memory_usage import profile_memory_usage
from .time import profile_time


def build_enabled_profilers() -> Callable:
    logger = get_logger()

    enabled_profilers = profiler_context.enabled_profilers
    logger.debug(f"Enabled profilers: {enabled_profilers}")

    return compose(
        (profile_memory_usage if "memory_usage" in enabled_profilers else identity),
        (profile_time if "time" in enabled_profilers else identity),
    )


__all__ = ["build_enabled_profilers"]