from typing import Callable, Any
from multiprocessing import Process, Manager, Queue
from threading import Event
from toolz import curry
from dowser.logger import get_logger
from dowser.common import lazy
from .synchronization import loop_until_sync, queue_to_list


def get_result(process: Process, queue: Queue) -> list[Any]:
    process.join()
    return queue_to_list(queue)


@curry
def parallelized_profiler(
    function: Callable,
    precision: float,
    *args,
    **kwargs,
) -> tuple[Callable, Event]:
    logger = get_logger()
    logger.debug(
        f"Setting up multiprocessing parallelized profiler for function {function.__name__}"
    )

    manager = Manager()
    queue = manager.Queue()
    sync_event = manager.Event()
    process = Process(
        target=loop_until_sync,
        args=(function, sync_event, queue, precision, *args),
        kwargs=kwargs,
    )
    process.start()

    result_handler = lazy(get_result)(process, queue)

    return result_handler, sync_event


__all__ = ["parallelized_profiler"]
