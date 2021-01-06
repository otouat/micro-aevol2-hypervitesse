import numpy as np
import pandas
from pathlib import Path, PurePath
import subprocess


CURRENT_FOLDER = Path().absolute()  # Current folder
PROJECT_HOME_FOLDER = CURRENT_FOLDER.parent  # Project root folder
EXEC_FILE = PROJECT_HOME_FOLDER / "cmake-build-debug" / "micro_aevol_cpu"
TRACE_CSV_FILE = CURRENT_FOLDER / "trace.csv"
STATS_BEST_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_best.csv"
STATS_MEAN_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_mean.csv"

FIXED_SEED = 42  # Always give that seed to the program.
FIRST_CHECKS_NBR_STEPS = 3


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


def first_checks():
    """
    These checks are necessary to ensure that there will not be any error in the upcoming commands.
    Some might seem uninteresting, such as checking CSVs, but it also helped me to learn Pandas and Numpy.
    Raises exceptions if anything is not ready.
    """

    # Ensure that the process can be run.
    assert EXEC_FILE.exists()
    call_program(just_help=True, timeout=.1)

    # Remove the CSV files if already existing to ensure that we will create new ones.
    TRACE_CSV_FILE.unlink(missing_ok=True)
    STATS_BEST_CSV_FILE.unlink(missing_ok=True)
    STATS_MEAN_CSV_FILE.unlink(missing_ok=True)

    # Quickly run process and ensure CSVs are okay.
    # Arguments are unrealistically small.
    call_program(
        nbr=FIRST_CHECKS_NBR_STEPS,
        width=5,  # Default value is 32
        height=5,  # Default value is 32
        genome_size=50,  # Default value is 5000
        seed=FIXED_SEED
    )

    # Check trace file
    assert TRACE_CSV_FILE.exists()
    trace_csv = pandas.read_csv(TRACE_CSV_FILE)
    assert trace_csv.shape == (FIRST_CHECKS_NBR_STEPS + 1, 7)

    for index, row in trace_csv.iterrows():
        assert row["Stamp"] == ("FirstEvaluation" if index == 0 else "STEP")
        current_duration = row["Duration"]
        assert np.issubdtype(int, type(current_duration))  # Ensure that it is an int
        assert current_duration  # Ensure not zero

    # Check stats files
    assert STATS_BEST_CSV_FILE.exists()
    best_csv = pandas.read_csv(STATS_BEST_CSV_FILE)
    assert best_csv.shape == (FIRST_CHECKS_NBR_STEPS, 10)

    assert STATS_MEAN_CSV_FILE.exists()
    mean_csv = pandas.read_csv(STATS_MEAN_CSV_FILE)
    assert mean_csv.shape == (FIRST_CHECKS_NBR_STEPS, 10)


def main():
    # First we ensure that all is okay.
    # So that no error will happen during the real script.
    first_checks()

    # TODO


if __name__ == "__main__":
    main()
