"""
Output Probability Oracle
"""
from os.path import dirname
from pathlib import Path
from typing import List, Tuple

from scipy.stats import chisquare
import simplejson

from results_accumulator import get_accumulated_results_by_input

def calculate_chi_square(
        expected_outputs_by_input_file_path: Path,
        observed_outputs_by_input_file_path: Path,
        measured_qubits_ids: List[int]):
    """
    Verifies expected results against actual results
    """
    with open(observed_outputs_by_input_file_path, 'r', encoding='utf-8') as file:
        observed_outputs_counts_by_input = simplejson.load(file)
    with open(expected_outputs_by_input_file_path, 'r', encoding='utf-8') as file:
        expected_outputs_probabilities_by_input = simplejson.load(file)

    accumulated_results_by_input = \
        get_accumulated_results_by_input(
                observed_outputs_counts_by_input,
                measured_qubits_ids)
    save_accumulated_observed_outputs(
        accumulated_results_by_input,
        observed_outputs_by_input_file_path)

    observed_outputs_counts_by_input = \
        match_observed_inputs_with_spec(
            accumulated_results_by_input,
            expected_outputs_probabilities_by_input
            )

    save_accumulated_observed_outputs(observed_outputs_counts_by_input,
                                      observed_outputs_by_input_file_path)

    total_counts_by_input = get_total_counts_by_input(
        observed_outputs_counts_by_input)

    expected_outputs_counts_by_input = \
        get_expected_outputs_counts_by_input(
            expected_outputs_probabilities_by_input,
            total_counts_by_input
        )

    save_expected_outputs_counts(expected_outputs_counts_by_input,
                                 expected_outputs_by_input_file_path)

    results = calculate_chisquare_for_each_input(
        observed_outputs_counts_by_input,
        expected_outputs_counts_by_input)

    # if len(wrong_outputs) > 0:
    #     save_wrong_outputs_by_input(wrong_outputs, observed_outputs_by_input_file_path)
    save_results(results, observed_outputs_by_input_file_path)
    return results

def get_observed_outputs_counts_by_input(
        observed_outputs_counts_by_input: dict,
        expected_outputs_probabilities_by_input: dict,
        measured_qubits_ids: List[int]):
    """
    get_observed_outputs_counts_by_input
    """
    return get_accumulated_results_by_input(
        remove_unexpecteds_by_input(
            observed_outputs_counts_by_input, \
            expected_outputs_probabilities_by_input),
        measured_qubits_ids
    )

def calculate_chisquare_for_each_input(
        observed_outputs_counts_by_input: dict,
        expected_outputs_counts_by_input: dict
        ) -> Tuple[dict, List]:
    """
    calculate the chi-square for each input
    """
    results_by_input = {}
    for input_value, expected_outputs_counts in \
        expected_outputs_counts_by_input.items():
        # [TODO] check WO
        observed_outputs_counts = \
            observed_outputs_counts_by_input.get(input_value)
        if observed_outputs_counts is not None:
            results_by_input[input_value] = \
                calculate_chisquare_from_counts(
                    expected_outputs_counts, observed_outputs_counts)
    return results_by_input

def calculate_chisquare_from_counts(
        expected_outputs_counts: dict,
        observed_outputs_counts: dict):
    """
    calculate_chisquare_from_counts
    """
    f_exp = []
    f_obs = []
    results = []
    for output, exp_count in expected_outputs_counts.items():
        f_exp = [ *f_exp, exp_count ]
        f_obs = [ *f_obs, observed_outputs_counts.get(output, 0) ]
    statistic, pvalue = chisquare(f_obs, f_exp)
    if statistic == .0 and pvalue is None:
        # exp and obs are equal
        pvalue = .0
    elif statistic == 100. and pvalue is None:
        pvalue = 1.
    results = [ *results, {
        "exp": expected_outputs_counts,
        "obs": observed_outputs_counts,
        "f_exp": f_exp, "f_obs": f_obs,
        "statistic": statistic, "pvalue": pvalue
        }]
    return results

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

def match_observed_inputs_with_spec(
        observed_outputs_counts_by_input: dict,
        expected_outputs_probabilities_by_input: dict) -> dict:
    """
    match_observed_inputs_spec
    """
    sample_input_value_from_observed = list(
        observed_outputs_counts_by_input.keys())[0]
    obs_input_len = len(sample_input_value_from_observed)

    sample_input_value_from_expected = list(
        expected_outputs_probabilities_by_input.keys())[0]
    exp_input_len = len(sample_input_value_from_expected)

    result = {}
    if exp_input_len <= obs_input_len:
        for input_value in expected_outputs_probabilities_by_input.keys():
            obs_input = input_value.zfill(obs_input_len)
            if obs_input in observed_outputs_counts_by_input:
                obs_outputs = observed_outputs_counts_by_input[obs_input]
                result[input_value] = obs_outputs
        return result

    message = "not implemented: observed inputs have less qubits " \
        + "than specification"
    raise NotImplementedError(message)

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

def remove_unexpecteds_by_input(
        observed_outputs_counts_by_input: dict,
        expected_outputs_probabilities_by_input: dict) -> dict:
    """
    remove_unexpecteds_by_input
    """
    return {
        input_value: remove_unexpected(
            observed_outputs_counts_by_input.get(input_value, {}),
            expected_outputs_probabilities
            ) for input_value, expected_outputs_probabilities in \
                expected_outputs_probabilities_by_input.items()
    }

def remove_unexpected(
        observed_outputs_counts: dict,
        expected_outputs_probabilities: dict) -> dict:
    """
    remove_unexpected
    """
    return {
        output: observed_outputs_counts.get(output, 0)
        for output in expected_outputs_probabilities.keys()
    }

def add_zero_probability_for_non_expected_outputs(
    expected_outputs_probabilities: dict,
    observed_outputs_counts: dict
    ):
    """
    adds 0 probability to the outputs when it is observed, but not expected
    """
    for output in observed_outputs_counts.keys():
        outputs_probabilities = expected_outputs_probabilities.get(output)
        if outputs_probabilities is None:
            # the output is not expected, but it was observed
            expected_outputs_probabilities[output] = .0
    return expected_outputs_probabilities

def add_zero_probability_for_non_expected_outputs_by_input(
        expected_outputs_probabilities_by_input: dict,
        observed_outputs_counts_by_input) -> dict:
    """
    adds 0 probability when the output is not expected, but it is observed
    """
    for input_value, observed_outputs_counts in \
        observed_outputs_counts_by_input.items():
        expected_outputs_probabilities_including_zeros = \
            add_zero_probability_for_non_expected_outputs(
                expected_outputs_probabilities_by_input[input_value],   # [FIXME][1] this will raise
                                                                        #   an exception it an input
                                                                        #   ran in the target
                                                                        #   circuit is not specified
                observed_outputs_counts
                )
        expected_outputs_probabilities_by_input[input_value] = \
            expected_outputs_probabilities_including_zeros
    return expected_outputs_probabilities_by_input

def add_zero_count_for_non_observed_outputs_by_input(
        observed_outputs_counts_by_input: dict,
        expected_outputs_probabilities_by_input: dict) -> dict:
    """
    adds 0 counts when the output is not observed, but it is expected
    """
    for input_value, expected_outputs_probabilities in \
        expected_outputs_probabilities_by_input.items():
        observed_outputs_counts_including_zeros = \
            add_zero_count_for_non_observed_outputs(
                observed_outputs_counts_by_input[input_value],  # [FIXME] this will raise an
                                                                #   exception if an specified
                                                                #   input was not run in the
                                                                #   target circuit
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
    file_name = f"{dirname(observed_results_file_path)}" \
        + f"/{observed_results_file_path.stem}.results.json"
    with open(file_name, 'w+', encoding="utf-8") as file:
        simplejson.dump(results, file, ignore_nan=True)

def save_accumulated_observed_outputs(
        accumulated_observed_outputs,
        observed_outputs_by_input_file_path: Path):
    """
    Save accumulated results into JSON file
    """
    file_name = f"{dirname(observed_outputs_by_input_file_path)}" \
        + f"/{observed_outputs_by_input_file_path.stem}.acc.json"
    with open(file_name, 'w+', encoding="utf-8") as file:
        simplejson.dump(accumulated_observed_outputs, file,
                        ignore_nan=True, indent=4)

def save_expected_outputs_counts(expected_outputs_counts_by_input: dict,
                                 expected_outputs_by_input_file_path: Path):
    """
    Save expected results counts into JSON file
    """
    file_name = f"{dirname(expected_outputs_by_input_file_path)}" \
        + f"/{expected_outputs_by_input_file_path.stem}.counts.json"
    with open(file_name, 'w+', encoding="utf-8") as file:
        simplejson.dump(expected_outputs_counts_by_input, file,
                        ignore_nan=True, indent=4)

def debug():
    """
    debug
    """
    expected_outputs_by_input_file_path = Path('E:\\2\\muskit\\QuantumSoftwareTestingTools\\Muskit\\' \
        + 'ExperimentalData\\QRAM\\QR_test_oracle.spec.json')
    observed_outputs_by_input_file_path = Path('E:\\2\\muskit\\QuantumSoftwareTestingTools\\Muskit\\' \
        + 'ExperimentalData\\QRAM\\json_results\\1AddGate_x_inGap_1_.json')
    measured_qubits_ids = [0, 1]
    calculate_chi_square(
        expected_outputs_by_input_file_path,
        observed_outputs_by_input_file_path,
        measured_qubits_ids)

if __name__ == "__main__":
    debug()
