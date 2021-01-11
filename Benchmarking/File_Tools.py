import subprocess
import numpy as np
import pandas
from typing import *
from Constants import *


def call_program(
        just_help: bool = False,
        nbr: int = None, width: int = None, height: int = None,
        mutation_rate: float = None, genome_size: int = None, seed: int = None,
        timeout: float = None
):
    """
    Helper function to call the program.
    Throws exception if exit code is not zero.
    Stdout and stderr are not shown.

    :param seed: adds argument "-s seed" (random generator seed)
    :param genome_size: adds argument "-g genome_size" (size of genome of each organism)
    :param mutation_rate: adds argument "-m mutation_rate" (rate of generated mutations)
    :param height: adds argument "-h height" (grid height)
    :param width: adds argument "-w width" (grid width)
    :param just_help: appends argument "--help" (show help and exit)
    :param nbr: appends argument "-n nbr" (number of generations)
    :param timeout: Ensures that it returns within that time, in seconds.
    """

    args = [EXEC_FILE, ]
    if just_help:
        args.append("--help")
    if nbr:
        args.append(f"-n{nbr}")
    if height:
        args.append(f"-h{height}")
    if width:
        args.append(f"-w{width}")
    if mutation_rate:
        args.append(f"-m{mutation_rate}")
    if genome_size:
        args.append(f"-g{genome_size}")
    if seed:
        args.append(f"-s{seed}")

    kwargs = {
        "args": args,
        "check": True,  # Ensure exit code is zero
        "capture_output": True,  # Don't output stdout and stderr in console
        "cwd": CURRENT_FOLDER,
    }
    if timeout:
        kwargs["timeout"] = timeout

    subprocess.run(**kwargs)


class TracesCSV:
    def __init__(self, duration_first_eval: int, duration_steps: List[int]):
        self.duration_first_eval = duration_first_eval
        self.duration_steps = duration_steps

        self.duration_steps_mean = np.mean(duration_steps)
        self.duration_steps_std = np.std(duration_steps)
        self.duration_steps_sum = np.sum(duration_steps)


def read_traces() -> TracesCSV:
    traces_dataframe = pandas.read_csv(TRACE_CSV_FILE)
    duration_first_evaluation: int = traces_dataframe.at[0, "Duration"]
    duration_steps: List[int] = []
    for index, row in traces_dataframe.iterrows():
        if index == 0:
            continue
        duration_steps.append(row["Duration"])
    return TracesCSV(duration_first_evaluation, duration_steps)
