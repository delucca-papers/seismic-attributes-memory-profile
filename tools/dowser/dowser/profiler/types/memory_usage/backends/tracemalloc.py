import time
import tracemalloc

from typing import Callable, Any
from toolz import compose
from functools import wraps
from dowser.logger import get_logger
from dowser.core import build_parallelized_profiler
from dowser.profiler.context import profiler_context
from ..types import MemoryUsageRecord


def to_memory_usage_record(traced_memory: tuple[int, int]) -> MemoryUsageRecord:
    timestamp = time.time()
    unit = "b"

    return timestamp, float(traced_memory[0]), unit


def get_traced_memory() -> tuple[int, int]:
    return tracemalloc.get_traced_memory()


tracemalloc_profiler = build_parallelized_profiler(
    compose(
        to_memory_usage_record,
        get_traced_memory,
    ),
    strategy="thread",
)


def profile_memory_usage(function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up tracemalloc memory usage profiler for function "{function.__name__}"'
    )

    pid = profiler_context.session_pid
    precision = profiler_context.memory_usage_precision

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        tracemalloc.start()
        hooked_function, get_memory_usage_profile = tracemalloc_profiler(
            function,
            precision,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_profile = get_memory_usage_profile()
        tracemalloc.stop()

        logger.debug(f"Amount of collected profile points: {len(memory_usage_profile)}")
        logger.debug(f"Sample data point: {memory_usage_profile[0]}")
        print(memory_usage_profile)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
