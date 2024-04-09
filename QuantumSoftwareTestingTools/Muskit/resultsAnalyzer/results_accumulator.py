"""
results accumulator accumulates the results counts depending
    on the qubits measured
"""
from typing import List

def accumulate_results_by_input(
    parsed_results_by_input: dict,
    qubits_ids: List[int],  # [TODO] should raise exception if len(qubits) > len(output)
                            #   => measuring more qubits than what the circuit has
    ) -> dict:
    """
    accumulates results for measured qubits, by input
    """
    return {
        input_value: accumulate_results(
            observed_outputs_counts, qubits_ids)
        for input_value, observed_outputs_counts \
        in parsed_results_by_input.items()
    }

def accumulate_results(
        observed_outputs_counts: dict,
        qubits_ids: List[int]
        ) -> dict:
    """
    accumulates results for measured qubits
    """
    results_accumulator = {}
    for observed_output, count in observed_outputs_counts.items():
        measured_qubits = get_measured_qubits(
            observed_output, qubits_ids)
        if measured_qubits in results_accumulator:
            results_accumulator[measured_qubits] += count
        else:
            results_accumulator[measured_qubits] = count
    return results_accumulator

def get_measured_qubits(
        observed_output: str,
        qubits_ids: List[int]) -> str:
    """
    get measured qubits from observed output
    """
    measured_qubits = ''
    qubits = list(observed_output)
    for qubit_id in qubits_ids:
        measured_qubits += qubits[qubit_id]
    return measured_qubits
