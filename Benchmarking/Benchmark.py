import numpy as np
import pandas
from pathlib import Path, PurePath
import subprocess
from typing import *
from time import time as ttime
import matplotlib.pyplot as plt


CURRENT_FOLDER = Path().absolute()  # Current folder
PROJECT_HOME_FOLDER = CURRENT_FOLDER.parent  # Project root folder
EXEC_FILE = PROJECT_HOME_FOLDER / "cmake-build-debug" / "micro_aevol_cpu"
TRACE_CSV_FILE = CURRENT_FOLDER / "trace.csv"
STATS_BEST_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_best.csv"
STATS_MEAN_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_mean.csv"

FIXED_SEED = 42  # Always give that seed to the program.
FIRST_CHECKS_NBR_STEPS = 3
DEFAULT_WIDTH = 32
DEFAULT_HEIGHT = 32
DEFAULT_MUTATION_RATE = 0.00001
DEFAULT_NB_STEPS = 1000
DEFAULT_GENOME_SIZE = 5000

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


def first_checks():
    """
    These checks are necessary to ensure that there will not be any error in the upcoming commands.
    Some might seem uninteresting, such as checking CSVs, but it also helped me to learn Pandas and Numpy.
    Raises exceptions if anything is not ready.
    """

    print("FIRST CHECKS ----- STARTING.")

    # Ensure that the process can be run.
    assert EXEC_FILE.exists()
    call_program(just_help=True, timeout=.1)

    print("Program can be called.")

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

    print("Trace.csv file is OK.")

    # Check stats files
    assert STATS_BEST_CSV_FILE.exists()
    best_csv = pandas.read_csv(STATS_BEST_CSV_FILE)
    assert best_csv.shape == (FIRST_CHECKS_NBR_STEPS, 10)

    assert STATS_MEAN_CSV_FILE.exists()
    mean_csv = pandas.read_csv(STATS_MEAN_CSV_FILE)
    assert mean_csv.shape == (FIRST_CHECKS_NBR_STEPS, 10)

    print("Stats CSV files are OK.")

    print("FIRST CHECKS ----- OK.")


def test_if_stats_are_deterministic() -> bool:
    """
    This function runs the program several time with the same arguments and compares the stats CSV files.
    It is made using different seeds to ensure no random stuff falsified our result.
    It outputs the conclusion.
    :return: True if deterministic, false otherwise.
    """
    NBR_STEPS = 25
    WIDTH = 10
    HEIGHT = 10
    GENOME_SIZE = 100
    MUTATION_RATE = 0.1234

    seeds = [1, 99999, 456]

    try:

        for seed in seeds:
            print(f"Testing with seed={seed}.")

            best_csv: List[pandas.DataFrame] = []
            mean_csv: List[pandas.DataFrame] = []

            for i in range(3):
                print(f"Run #{i}.")
                call_program(
                    nbr=NBR_STEPS,
                    width=WIDTH,
                    height=HEIGHT,
                    mutation_rate=MUTATION_RATE,
                    genome_size=GENOME_SIZE,
                    seed=seed
                )
                best_csv.append(pandas.read_csv(STATS_BEST_CSV_FILE))
                mean_csv.append(pandas.read_csv(STATS_MEAN_CSV_FILE))

            assert best_csv[0].equals(best_csv[1])
            assert best_csv[0].equals(best_csv[2])
            assert mean_csv[0].equals(mean_csv[1])
            assert mean_csv[0].equals(mean_csv[2])

        print("Conclusion: program runs are deterministic if we only look at statistics CSV files.")
        print("In other words, calling the program with the same arguments will produce the exact same results.")
        return True

    except AssertionError:
        print("Conclusion: program runs are non-deterministic if we only look at statistics CSV files.")
        print("In other words, calling the program with the same arguments will produce different results.")
        return False


def time_different_grid_sizes():
    NB_TRIES = 3
    CURRENT_GENOME_SIZE = 500
    CURRENT_NB_STEPS = 200

    values_to_check = [8, 16, 32, 48, ]#64, 96, 128]
    results = {}

    with open("my_outputs.csv", "w") as f:
        f.write("SEP=,\n")
        f.write("Width, Height, FirstEvaluation, Step(Mean)\n")

        for width in values_to_check:
            for height in values_to_check:
                first_eval_list = []
                steps_mean_list = []

                for i in range(NB_TRIES):
                    try:
                        call_program(
                            width=width, height=height,
                            seed=FIXED_SEED, mutation_rate=DEFAULT_MUTATION_RATE, genome_size=CURRENT_GENOME_SIZE,
                            nbr=CURRENT_NB_STEPS
                        )
                        traces = read_traces()
                        first_eval_list.append(traces.duration_first_eval)
                        steps_mean_list.append(traces.duration_steps_mean)
                    except:
                        pass

                if first_eval_list and steps_mean_list:
                    first_eval = int(np.mean(first_eval_list))
                    steps_mean = int(np.mean(steps_mean_list))
                    print(f"For width={width} and height={height}, we have: first eval={first_eval} and mean step duration={steps_mean}")
                    f.write(f"{width}, {height}, {first_eval}, {steps_mean}\n")
                    results[width, height] = (first_eval, steps_mean)
                else:
                    print(f"Unable to test with width={width} and height={height}")

    with open("my_outputs2.csv", "w") as f:
        f.write("SEP=,\n")
        f.write("Size, FirstEvaluation, Step(Mean)\n")

        sizes = [int(k[0] * k[1]) for k in results.keys()]
        first_evals = [int(v[0] / 1e3) for v in results.values()]
        step_means = [int(v[1] / 1e3) for v in results.values()]

        for i in range(len(sizes)):
            f.write(f"{sizes[i]},{first_evals[i]},{step_means[i]}\n")

        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel("Taille de la grille")
        ax1.set_ylabel("FirstEvaluation", color=color)
        ax1.plot(sizes, first_evals, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = "tab:blue"
        ax2.set_ylabel("Step (moyenne)", color=color)
        ax2.plot(sizes, step_means, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()

        """
        axis1 = plt.plot(sizes, first_evals, marker='o')
        axis2 = plt.plot(sizes, step_means, 'v')
        # plt.xlabel("Tailles de la grille")
        # plt.ylabel("Durée de 'FirstEvaluation' en ms")
        plt.legend([axis1, axis2], ['FirstEvaluation', 'Step (moyenne)'])
        """
        plt.title("Durées (en us) en fonction de la taille de la grille")
        plt.savefig("GridSizes.png")



def main():
    # First we ensure that all is okay.
    # So that no error will happen during the real script.
    first_checks()
    #test_if_stats_are_deterministic()
    time_different_grid_sizes()

    # TODO


if __name__ == "__main__":
    main()
