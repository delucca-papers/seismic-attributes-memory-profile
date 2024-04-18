from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.edge_detection import EigComplex
    from common.cluster import run_attribute

    quality = EigComplex()

    return run_attribute(quality, input, n_workers, single_threaded)