"""
Tests for the results_accumulator module
"""
import pytest

from results_accumulator import \
    accumulate_results, \
    accumulate_results_by_input


@pytest.mark.parametrize(
        "counts,qubits_ids,expected", [
            (
                { "0000001": 24, "0000101": 76 },
                [0, 1],
                { "00": 100 }),
            (
                { "0000001": 20, "0000101": 70, "1000000": 10 },
                [0, 1, 6],
                { "001": 90, "100": 10 }),
            (
                { "0000001": 24, "0000101": 76 },
                [2, 4],
                { "00": 24, "01": 76 }),
            ])
def test_should_accumulate_results(counts, qubits_ids, expected):
    """
    test_should_accumulate_results
    """
    # when
    result = accumulate_results(counts, qubits_ids)

    # then
    assert result == expected

def test_should_accumulate_results_by_input():
    """
    test_should_accumulate_results_by_input
    """
    # given
    observed_outputs_counts_by_input = {
        "0000000": { "0000001": 24, "0000101": 76 },
        "0000001": { "0001001": 29, "0001101": 71 },
        "0000011": { "0011001": 29, "0011101": 71 },
        "0001000": { "0000010": 22, "0100101": 78 },
        "1011000": { "1100111": 73, "1000000": 27 },
        "1011001": { "1001000": 18, "1101111": 82 }
    }
    qubits_ids = [0, 1]

    # when
    result = accumulate_results_by_input(
        observed_outputs_counts_by_input, qubits_ids)

    # then
    assert result == {
        "0000000": { "00": 100 },
        "0000001": { "00": 100 },
        "0000011": { "00": 100 },
        "0001000": { "00": 22, "01": 78 },
        "1011000": { "11": 73, "10": 27 },
        "1011001": { "10": 18, "11": 82 }
    }
