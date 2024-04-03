"""
Output Probability Oracle
"""
from pathlib import Path
from scipy.stats import chisquare
import simplejson

def verify(expected_results_file_path: Path, observed_results_file_path: Path, pvalue: float):
    """
    Verifies expected results against actual results for a given input
    """
    with open(observed_results_file_path, 'r', encoding='utf-8') as file:
        observed_results = simplejson.load(file)
    with open(expected_results_file_path, 'r', encoding='utf-8') as file:
        expected_results = simplejson.load(file)
    for input_value, observed_results_counts in observed_results.items():
        r = calculate_chi_square(
            expected_results[input_value], # |
                # KeyError here means we've got an unspecified output
                # should raise WOO
            observed_results_counts
        )
        print(r)

def get_exp_and_obs_frequencies(
        expected_results_counts: dict, observed_results_counts: dict
        ) -> dict:
    """
    get expected and observed (actual) frequencies
    """
    exp = []
    obs = []
    for o, c in expected_results_counts.items():
        exp = [ *exp, c ]
        obs = [ *obs, observed_results_counts.get(o, 0)] # |
            # if the output is not observed, it's 0 counts
    return { "exp": exp, "obs": obs }

def calculate_chi_square(
        expected_results_probabilities: dict,
        observed_results_counts: dict):
    """
    calculate Chi-Square from observed (actual) results relative
        to the expected results
    """
    n_shots = get_n_shots(observed_results_counts)
    expected_results_counts = get_expected_counts_table(
        expected_results_probabilities, n_shots)
    f = get_exp_and_obs_frequencies(
        expected_results_counts, observed_results_counts)
    return chisquare(f['obs'], f['exp'])

def get_n_shots(counts_by_input: dict):
    """
    returns the number of "shots" (simulation runs) for a given input
    """
    return sum(counts_by_input.values())

def get_expected_counts_table(expected_probabilities_by_input: dict, n_shots: int):
    """
    returns a contingency table obtained from the expected results for a given
        input
    """
    return {
        k: int(round(v * n_shots))
        for k, v in expected_probabilities_by_input.items()
    }
