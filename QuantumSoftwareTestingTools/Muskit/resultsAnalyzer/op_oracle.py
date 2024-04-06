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
        observed_outputs_by_input = simplejson.load(file)
    with open(expected_outputs_by_input_file_path, 'r', encoding='utf-8') as file:
        expected_outputs_by_input = simplejson.load(file)

    # wrong_outputs = []
    # expected_outputs_by_input = expected_outputs_by_input.get(input_value) # |
    #         # None means a Wrong Output was observed
    #     if expected_outputs_by_input is None:
    #         wrong_outputs = [
    #             *wrong_outputs,
    #             { "input": input_value, "outputs": observed_outputs_counts }
    #         ]
    total_observed_output_counts, total = \
        get_total_observed_output_counts(observed_outputs_by_input)
    total_expected_output_counts = \
        get_total_expected_output_counts(expected_outputs_by_input, total)

        # else:
        #     r = calculate_chi_square(
        #         expected_results[input_value], # |
        #             # KeyError here means we've got an unspecified output
        #             # should raise WOO
        #         observed_results_counts
        #     )
        #     statistic, pvalue = r
        #     results = [
        #         *results, {
        #             "statistic": statistic,
        #             "pvalue": pvalue,
        #             "input": input_value
        #             } ]
    # if len(wrong_outputs) > 0:
    #     save_wrong_outputs_by_input(wrong_outputs, observed_outputs_by_input_file_path)
    # save_results(results, observed_results_file_path)

def get_total_observed_output_counts(
        observed_outputs_by_input: dict
        ) -> Tuple[dict, int]:
    """
    returns the total output counts considering all inputs
    """
    total_observed_output_counts = {}
    total = 0
    for observed_outputs_counts in observed_outputs_by_input.values():
        for output, counts in observed_outputs_counts.items():
            if output in total_observed_output_counts:
                total_observed_output_counts[output] += counts
            else:
                total_observed_output_counts[output] = counts
            total += counts
    return total_observed_output_counts, total

def get_total_expected_output_counts(
        expected_outputs_probabilities_by_input: dict,
        total_observed_counts: int
        ) -> dict:
    """
    gets the total expected output counts from the expected probabilities
        given the total number of outputs observed
    """
    expected_output_counts = {}
    total = 0
    for expected_outputs_probabilities in expected_outputs_probabilities_by_input.values():
        for output, probability in expected_outputs_probabilities.items():
            count = probability * 100
            if output in expected_output_counts:
                expected_output_counts[output] += count
            else:
                expected_output_counts[output] = count
            total += count
    scale = total_observed_counts / total
    return {
        output: counts * scale
        for output, counts in expected_output_counts.items()
    }

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
