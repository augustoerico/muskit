"""
Utility functions
"""
from typing import List

def fix_number_of_qubits(outputs_probabilities_by_input: dict) -> dict:
    """
    add zeros to the left to match input and output qubit counts
        separately
    """
    inputs = outputs_probabilities_by_input.keys()
    max_n_qubits_input = get_len_qubits_in_input(inputs)

    outputs_probabilities = outputs_probabilities_by_input.values()
    max_n_qubits_output = get_len_qubits_in_output(outputs_probabilities)

    result = {}
    for input_value, outputs_probabilities in \
        outputs_probabilities_by_input.items():
        result[input_value.zfill(max_n_qubits_input)] = {
            output.zfill(max_n_qubits_output): probability
            for output, probability in \
            outputs_probabilities.items()
            }

    return result

def get_len_qubits_in_output(
        outputs_probabilities: List[dict]) -> int:
    """
    get_len_qubits_in_output
    """
    max_len_qubits = 0
    for i in outputs_probabilities:
        for output in i.keys():
            len_qubits = len(output)
            if len_qubits > max_len_qubits:
                max_len_qubits = len_qubits
    return max_len_qubits

def get_len_qubits_in_input(inputs: List[str]) -> int:
    """
    get_len_qubits_in_input
    """
    max_len_qubits = 0
    for i in inputs:
        len_qubits = len(i)
        if len_qubits > max_len_qubits:
            max_len_qubits = len_qubits
    return max_len_qubits
