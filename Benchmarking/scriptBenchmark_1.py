import subprocess
import numpy as np
from pathlib import Path
import pandas
from typing import List

"""
This is a simpler version of the Python scripts. 
We used this one for actual benchmarks.
"""

CURRENT_FOLDER = Path().absolute()
PROJECT_HOME_FOLDER = CURRENT_FOLDER.parent
EXEC_FILE = PROJECT_HOME_FOLDER / "cmake-build-release" / "micro_aevol_cpu"
TRACE_CSV_FILE = CURRENT_FOLDER / "trace.csv"
NBR_REP = 25


def runbench_time():
    steps = [1000, 5000, 10000]
    for s in steps:
        L = []
        for i in range(NBR_REP):
            y = subprocess.run(
                ["time", "-f", "%e", "--output=tmp.txt", EXEC_FILE, f"-n{s}"],
               capture_output=True, check=True
            )
            with open("tmp.txt", "r") as f:
                L.append(float(f.readlines()[0]))
        print(
            "resultat nbstep= ", s, "moyenne= ", round(np.mean(L), 3),
            "median= ", round(np.median(L), 3), "std= ", round(np.std(L), 3)
        )
    return 0


def runbench_trace_steps():
    steps = [1000, 5000, 10000]
    for s in steps:
        y = subprocess.run(
            [EXEC_FILE, f"-n{s}"],
            capture_output=False, check=True
        )
        traces_dataframe = pandas.read_csv(TRACE_CSV_FILE)
        duration_steps: List[float] = []
        first_evaluation = 0
        for index, row in traces_dataframe.iterrows():
            if index == 0:
                first_evaluation = row["Duration"] / 1e6
            else:
                duration_steps.append(row["Duration"] / 1e6)
        print(
            "resultat (by steps) nbstep= ", s, "moyenne= ", round(np.mean(duration_steps), 2),
            "median= ", round(np.median(duration_steps), 2), "std= ", round(np.std(duration_steps), 2),
            "FirstEvaluation= ", first_evaluation
        )
    return 0


runbench_time()
# runbench_trace_steps()
