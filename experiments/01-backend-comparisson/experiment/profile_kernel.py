import os

from dowser import profile
from dowser.adapters import Logger
from consume_large_memory import consume_large_memory

logger = Logger("ProfileKernel")

if __name__ == "__main__":
    logger.info("Starting kernel backend experiment")

    num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    input_metadata = f"num_elements={num_elements}"

    logger.info(f"Running experiment with {num_elements} elements")
    profile(consume_large_memory, input_metadata=input_metadata)(num_elements)
