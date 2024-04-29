from argparse import _SubParsersAction
from dowser.common.cli import AppendUnique
from .main import run_profiler


__all__ = ["attach_profiler_args"]


def attach_profiler_args(subparsers: _SubParsersAction) -> _SubParsersAction:
    profile_parser = subparsers.add_parser(
        "profile",
        help="Profile enabled metrics of a Python program",
    )

    profile_parser.add_argument(
        "--enable-metric",
        "-m",
        help="Enables metric to use on the profiling session (default: memory_usage,time)",
        choices=["memory_usage", "time"],
        action=AppendUnique,
    )

    profile_parser.add_argument(
        "--enable-mem-backend",
        "-b",
        help="Enable memory usage backend for the profiling session (default: psutil,resource,tracemalloc,mprof,kernel)",
        choices=["psutil", "resource", "tracemalloc", "mprof", "kernel"],
        action=AppendUnique,
    )

    profile_parser.add_argument(
        "--mem-unit",
        help="Unit to use for the memory usage (default: mb)",
        choices=["kb", "mb", "gb"],
    )

    profile_parser.add_argument(
        "--session-id",
        help="Session ID to use for the profiling session (default: random UUID4)",
    )

    profile_parser.add_argument("filepath", help="Path to the Python file to execute")

    profile_parser.add_argument(
        "--entrypoint",
        "-e",
        help="Function to use as entrypoint of your file (default: __main__)",
    )

    profile_parser.add_argument(
        "--kwargs",
        nargs="*",
        help="Keyword arguments that will be passed to your function in the format key=value",
        action="append",
        default={},
    )

    profile_parser.add_argument(
        "args",
        nargs="*",
        help="Arguments that will be passed to your function",
        type=tuple,
        default=tuple(),
    )

    profile_parser.set_defaults(func=run_profiler)

    return subparsers