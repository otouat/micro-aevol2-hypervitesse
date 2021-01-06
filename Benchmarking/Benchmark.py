import numpy as np
import pandas
from pathlib import Path, PurePath
import subprocess


current_folder = Path().absolute()  # Current folder
project_home = current_folder.parent  # Project root folder
exec_file = project_home / "cmake-build-debug" / "micro_aevol_cpu"
assert exec_file.exists()

trace_file = current_folder / "trace.csv"
stats_best_file = current_folder / "stats" / "stats_simd_best.csv"
stats_mean_file = current_folder / "stats" / "stats_simd_mean.csv"


def first_checks():
    # Ensure that the process can be run.
    subprocess.run(
        args=[exec_file, "--help"],  # Just the "help" command to ensure it is okay
        timeout=.1,  # Ensure the time is reasonable for such a simple command
        check=True,  # Ensure exit code is zero
        capture_output=True  # Don't output stdout and stderr in console
    )

    # Quickly run process and ensure CSVs are okay.
    subprocess.run(
        args=[exec_file, "-n", "10"],
        check=True,
        capture_output=True
    )
    # Check trace file
    assert trace_file.exists()
    trace_csv = pandas.read_csv(trace_file)
    print(trace_csv.shape)
    assert trace_csv.shape == (10+1, 7)
    assert trace_csv.at[0, "Stamp"] == "FirstEvaluation"
    first_eval_duration = trace_csv.at[0, "Duration"]
    assert np.issubdtype(int, type(first_eval_duration))  # Ensure that it is an int
    assert first_eval_duration  # Ensure not zero
    assert trace_csv.at[1, "Stamp"] == "STEP"
    step_0_duration = trace_csv.at[1, "Duration"]
    assert np.issubdtype(int, type(step_0_duration))  # Ensure that it is an int
    assert step_0_duration  # Ensure not zero

    # Check stats files
    # TODO
    assert stats_best_file.exists()
    assert stats_mean_file.exists()


def main():
    first_checks()
    # TODO


if __name__ == "__main__":
    main()
