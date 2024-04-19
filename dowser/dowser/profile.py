from typing import Callable
from logging import Logger
from toolz import compose, identity
from .core.config import extend_config, get_namespace
from .core.logging import get_logger
from .profilers import execution_time, memory_usage


def profile(function: Callable, config: dict = {}):
    logger = get_logger()
    logger.info(f'Setting up profilers for function "{function.__name__}"')
    logger.debug(f"Custom config: {config}")

    config = extend_config(config)
    profiler_config = get_namespace("profiler", config)
    enabled_profilers = profiler_config.get("enabled_profilers").split(",")

    with_profilers = compose(
        (
            memory_usage.profile(config=config)
            if "memory_usage" in enabled_profilers
            else identity
        ),
        (
            execution_time.profile(config=config)
            if "execution_time" in enabled_profilers
            else identity
        ),
    )

    return with_profilers(function)


__all__ = ["profile"]
