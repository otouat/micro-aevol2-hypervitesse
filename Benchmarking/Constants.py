from pathlib import Path


CURRENT_FOLDER = Path().absolute()  # Current folder
PROJECT_HOME_FOLDER = CURRENT_FOLDER.parent  # Project root folder
HAS_TRACE_CSV_FILE = True
TRACE_CSV_FILE = CURRENT_FOLDER / "trace.csv"
STATS_BEST_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_best.csv"
STATS_MEAN_CSV_FILE = CURRENT_FOLDER / "stats" / "stats_simd_mean.csv"
ENABLE_TRACES_CSV_IF_RELEASE = False  # On Release, if True, then the "traces.csv" file is expected.
FORCE_RELEASE = True  # If true then we always go for Release.


def _get_most_recent_exec_file() -> Path:
    debug_file = PROJECT_HOME_FOLDER / "cmake-build-debug" / "micro_aevol_cpu"
    release_file = PROJECT_HOME_FOLDER / "cmake-build-release" / "micro_aevol_cpu"

    debug_mtime = debug_file.stat().st_mtime
    release_mtime = release_file.stat().st_mtime

    if debug_mtime <= release_mtime or FORCE_RELEASE:
        # Return release exec file if most recent, and kill "traces.csv" data.
        if not ENABLE_TRACES_CSV_IF_RELEASE:
            global HAS_TRACE_CSV_FILE, TRACE_CSV_FILE
            HAS_TRACE_CSV_FILE = False
            # del TRACE_CSV_FILE
        return release_file
    else:
        # Return debug exec file if most recent.
        return debug_file


EXEC_FILE = _get_most_recent_exec_file()

FIXED_SEED = 42  # Always give that seed to the program.
FIRST_CHECKS_NBR_STEPS = 3
DEFAULT_WIDTH = 32
DEFAULT_HEIGHT = 32
DEFAULT_MUTATION_RATE = 1e-5
DEFAULT_NB_STEPS = 1000
DEFAULT_GENOME_SIZE = 5000

QUICK_RUNS_GENOME_SIZE = 500
QUICK_RUNS_NB_STEPS = 200
QUICK_RUNS_WIDTH = 16
QUICK_RUNS_HEIGHT = 16
QUICK_RUNS_MUTATION_RATE = 1e-8

TIME_FUNCTIONS_NUMBER_REPETITIONS = 3
