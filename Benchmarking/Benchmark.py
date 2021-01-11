import numpy as np
import pandas
from typing import *
from Constants import *
from File_Tools import *
from Stats_Maker import *


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

    seeds = [1, 99999, 456]

    try:

        for seed in seeds:
            print(f"Testing with seed={seed}.")

            best_csv: List[pandas.DataFrame] = []
            mean_csv: List[pandas.DataFrame] = []

            for i in range(3):
                print(f"Run #{i}.")
                call_program(
                    nbr=QUICK_RUNS_NB_STEPS,
                    width=QUICK_RUNS_WIDTH,
                    height=QUICK_RUNS_HEIGHT,
                    mutation_rate=QUICK_RUNS_MUTATION_RATE,
                    genome_size=QUICK_RUNS_GENOME_SIZE,
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
    values_to_check = [8, 16, 32, 48, ]#64, 96, 128]
    results = {}

    for width in values_to_check:
        for height in values_to_check:
            first_eval_list = []
            steps_mean_list = []

            for i in range(TIME_FUNCTIONS_NUMBER_REPETITIONS):
                try:
                    call_program(
                        width=width, height=height,
                        seed=FIXED_SEED, mutation_rate=QUICK_RUNS_MUTATION_RATE, genome_size=QUICK_RUNS_GENOME_SIZE,
                        nbr=QUICK_RUNS_NB_STEPS
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
                results[width, height] = (first_eval, steps_mean)
            else:
                print(f"Unable to test with width={width} and height={height}")

    # Make stats
    sizes = [int(k[0] * k[1]) for k in results.keys()]
    first_evals = [int(v[0] / 1e3) for v in results.values()]
    step_means = [int(v[1] / 1e3) for v in results.values()]

    make_stats_file("grid_size", "grid_size", sizes, first_evals, step_means)
    make_stats_diagram("grid_size", "Size of the grid", sizes, first_evals, step_means)


def time_genome_sizes():
    values_to_check = [250, 500, 1000, 2000, 5000, 10000, 20000]
    results = {}

    for genome_size in values_to_check:
        first_eval_list = []
        steps_mean_list = []

        for i in range(TIME_FUNCTIONS_NUMBER_REPETITIONS):
            try:
                call_program(
                    width=QUICK_RUNS_WIDTH, height=QUICK_RUNS_HEIGHT,
                    seed=FIXED_SEED, mutation_rate=QUICK_RUNS_MUTATION_RATE, genome_size=genome_size,
                    nbr=QUICK_RUNS_NB_STEPS
                )
                traces = read_traces()
                first_eval_list.append(traces.duration_first_eval)
                steps_mean_list.append(traces.duration_steps_mean)
            except:
                pass

        if first_eval_list and steps_mean_list:
            first_eval = int(np.mean(first_eval_list))
            steps_mean = int(np.mean(steps_mean_list))
            print(f"For genome_size={genome_size}, we have: first eval={first_eval} and mean step duration={steps_mean}")
            results[genome_size] = (first_eval, steps_mean)
        else:
            print(f"Unable to test with genome_size={genome_size}")

    # Make stats
    sizes = [int(k) for k in results.keys()]
    first_evals = [int(v[0] / 1e3) for v in results.values()]
    step_means = [int(v[1] / 1e3) for v in results.values()]

    make_stats_file("genome_size", "genome_size", sizes, first_evals, step_means)
    make_stats_diagram("genome_size", "Size of the genome", sizes, first_evals, step_means)


def main():
    # First we ensure that all is okay.
    # So that no error will happen during the real script.
    first_checks()
    test_if_stats_are_deterministic()
    # time_different_grid_sizes()
    time_genome_sizes()

    # TODO


if __name__ == "__main__":
    main()
