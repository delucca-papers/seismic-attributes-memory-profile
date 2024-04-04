from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.signal import TimeGain
    from common.cluster import run_attribute

    quality = TimeGain()

    return run_attribute(quality, input, n_workers, single_threaded)
