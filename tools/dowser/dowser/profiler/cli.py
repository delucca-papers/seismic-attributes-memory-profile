from argparse import _SubParsersAction
from dowser.common.cli import AppendUnique
from .main import run_profiler


__all__ = ["attach_args"]


def attach_args(subparsers: _SubParsersAction) -> _SubParsersAction:
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
        "--profiler-session-id",
        help="Session ID to use for the profiling session (default: random UUID4)",
    )

    profile_parser.add_argument(
        "-d",
        "--profiler-depth",
        help="Define the depth of the profiler when using the instrumentation strategy (default: 3, use -1 to disable depth limit)",
    )

    profile_parser.add_argument(
        "-s",
        "--profiler-strategy",
        help="Define the strategy to use for the profiler (default: sampling)",
    )

    profile_parser.add_argument(
        "--profiler-precision",
        help="Define the precision to use for the profiler (default: 2)",
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
