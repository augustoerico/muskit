"""
Output Probability Oracle
"""
from os.path import dirname
from pathlib import Path
from typing import List, Tuple

from scipy.stats import chisquare
import simplejson

def verify(
        expected_outputs_by_input_file_path: Path,
        observed_outputs_by_input_file_path: Path,
        pvalue: float):
    """
    Verifies expected results against actual results for a given input
    """
    with open(observed_outputs_by_input_file_path, 'r', encoding='utf-8') as file:
        observed_outputs_counts_by_input = simplejson.load(file)
    with open(expected_outputs_by_input_file_path, 'r', encoding='utf-8') as file:
        expected_outputs_probabilities_by_input = simplejson.load(file)

    observed_outputs_counts_by_input = \
        add_zero_count_for_non_observed_outputs(
            observed_outputs_counts_by_input,
            expected_outputs_probabilities_by_input
        )
    total_counts_by_input = get_total_counts_by_input(
        observed_outputs_counts_by_input)
    expected_outputs_counts_by_input = \
        get_expected_outputs_counts_by_input(
            expected_outputs_probabilities_by_input,
            total_counts_by_input
        )
    # results, wrong_outputs = calculate_chisquare_for_each_input(
    #     observed_outputs_counts_by_input,
    #     expected_outputs_probabilities_by_input)

    # wrong_outputs = []
    # expected_outputs_by_input = expected_outputs_by_input.get(input_value) # |
    #         # None means a Wrong Output was observed
    #     if expected_outputs_by_input is None:
    #         wrong_outputs = [
    #             *wrong_outputs,
    #             { "input": input_value, "outputs": observed_outputs_counts }
    #
    # if len(wrong_outputs) > 0:
    #     save_wrong_outputs_by_input(wrong_outputs, observed_outputs_by_input_file_path)
    # save_results(results, observed_results_file_path)

def get_expected_outputs_counts_by_input(
        expected_outputs_probabilities_by_input: dict,
        total_counts_by_input
        ) -> dict:
    """
    returns the expected outputs counts for each input, given
        the total counts of observed outputs for each input
    """
    return {
        input_value: \
            get_expected_outputs_counts(
                expected_outputs_probabilities,
                total_counts_by_input[input_value])
        for input_value, expected_outputs_probabilities in \
            expected_outputs_probabilities_by_input.items()
    }

def get_expected_outputs_counts(
        expected_outputs_probabilities: dict,
        total_counts: int
        ) -> dict:
    """
    returns the expected output counts given a total counts
    """
    return {
        output: round(probability * total_counts)
        for output, probability in \
            expected_outputs_probabilities.items()
    }

def add_zero_count_for_non_observed_outputs_by_input(
        observed_outputs_counts_by_input: dict,
        expected_outputs_probabilities_by_input: dict) -> dict:
    """
    adds 0 counts when the output is not observed, but is expected
    """
    for input_value, expected_outputs_probabilities in \
        expected_outputs_probabilities_by_input.items():
        observed_outputs_counts_including_zeros = \
            add_zero_count_for_non_observed_outputs(
                observed_outputs_counts_by_input[input_value],
                expected_outputs_probabilities)
        observed_outputs_counts_by_input[input_value] = \
            observed_outputs_counts_including_zeros
    return observed_outputs_counts_by_input

def add_zero_count_for_non_observed_outputs(
        observed_outputs_counts: dict,
        expected_outputs_probabilities: dict) -> dict:
    """
    adds 0 counts to observed outputs when it is not observed, but
        it is expected
    """
    for output in expected_outputs_probabilities.keys():
        output_counts = observed_outputs_counts.get(output)
        if output_counts is None:
            # the output is not observed, but is expected
            observed_outputs_counts[output] = 0
    return observed_outputs_counts

# def calculate_chisquare_for_each_input(
#         observed_outputs_counts_by_input: dict,
#         expected_outputs_probabilities_by_input: dict
#         ) -> Tuple[dict, List]:
#     """
#     calculate the chi-square for each input
#     """
#     wrong_outputs = [] # observed output that is not expected
#     for input_value, observed_outputs_counts in \
#         observed_outputs_counts_by_input.items():
#         total_counts = get_total_counts(observed_outputs_counts)

#         # get_expected_output(expected_outputs_probabilities, total_counts)

def get_total_counts_by_input(
        observed_outputs_counts_by_input: dict) -> int:
    """
    get total counts from an observed outputs
    """
    total_counts_by_input = {}
    for input_value, observed_outputs_counts in \
        observed_outputs_counts_by_input.items():
        total_counts_by_input[input_value] = sum(observed_outputs_counts.values())
    return total_counts_by_input

def save_wrong_outputs_by_input(
        wrong_outputs: List[dict],
        observed_results_file_path: Path
        ) -> None:
    """
    Save Wrong Outputs list by a given input
    """
    file_name = f"{dirname(observed_results_file_path)}" \
        + f"/{observed_results_file_path.stem}.woo.json"
    with open(file_name, 'w', encoding="utf-8") as file:
        simplejson.dump(wrong_outputs, file, ignore_nan=True, indent=4)

def save_results(results: List, observed_results_file_path: Path):
    """
    Save results into JSON file
    """
    print('asdfasdfasdfa')
    file_name = f"{dirname(observed_results_file_path)}" \
        + f"/{observed_results_file_path.stem}.results.json"
    with open(file_name, 'w', encoding="utf-8") as file:
        simplejson.dump(results, file, ignore_nan=True, indent=4)
