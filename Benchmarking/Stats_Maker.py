from typing import *
import matplotlib.pyplot as plt


def make_stats_file(
        filename: str,
        field_name: str, field_values: List[int],
        first_evals: List[int], step_means: List[int]
):
    """
    Creates a file with extension ".CSV" and the given data. All lists must be the same length.
    Times should be in microseconds.

    :param filename: name of the file to be created, without extension.
    :param field_name: name of the field to be written in the CSV header.
    :param field_values: values of that field.
    :param first_evals: values of "FirstEvaluation".
    :param step_means: mean values of "STEP".
    """

    assert len(field_values) == len(first_evals) == len(step_means)

    with open(f"{filename}.csv", "w") as f:
        f.write("SEP=,\n")
        f.write(f"{field_name}, FirstEvaluation, Step(Mean)\n")

        for i in range(len(field_values)):
            f.write(f"{field_values[i]},{first_evals[i]},{step_means[i]}\n")


def make_stats_diagram(
        filename: str,
        field_description: str, field_values: List[int],
        first_evals: List[int], step_means: List[int]
):
    """

    Creates a graph file with extension ".PNG" and the given data.
    It will show two plots in the same image, both having that given field as X axis
    and the Y axises are both time measurements.
    All lists must be the same length. Times should be in microseconds.

    :param filename: name of the file to be created, without extension.
    :param field_description: text which will appear as legend of the X axis.
    :param field_values: values of that field.
    :param first_evals: values of "FirstEvaluation".
    :param step_means: mean values of "STEP".
    """

    # First plot
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel(field_description)
    ax1.set_ylabel("FirstEvaluation", color=color)
    ax1.plot(field_values, first_evals, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Second plot
    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.set_ylabel("Step (moyenne)", color=color)
    ax2.plot(field_values, step_means, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()

    plt.savefig(f"{filename}.png")
