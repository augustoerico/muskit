"""
Tests for utils module
"""
from utils import get_len_qubits_in_input, \
    get_len_qubits_in_output, fix_number_of_qubits

def test_should_get_outputs_qubits_length():
    """
    test_should_get_outputs_qubits_length
    """
    # given
    outputs_probabilities = [
        { "1": .2, "10": .2, "101": .4, "11": .2 },
        { "0": .5, "1": .5 }, { "11": .3, "1": .6, "0": .1 }
    ]

    # when
    result = get_len_qubits_in_output(outputs_probabilities)

    # then
    assert result == 3

def test_should_get_input_qubits_length():
    """
    test_should_get_input_qubits_length
    """
    # given
    inputs = [ "0", "1", "10", "11", "100" ]

    # when
    result = get_len_qubits_in_input(inputs)

    #  then
    assert result == 3

def test_should_fix_the_length_of_qubits_in_parsed_outputs_probabilities_by_input():
    """
    test_should_fix_the_length_of_qubits_in_parsed_outputs_probabilities_by_input
    """
    # given
    outputs_probabilities_by_input = {
        "1": { "1": .2, "10": .2, "0": .4, "11": .2 },
        "1001": { "0": .5, "1": .5 },
        "11": { "11": .3, "1": .6, "0": .1 }
    }

    # when
    result = fix_number_of_qubits(outputs_probabilities_by_input)

    # then
    assert result == {
        "0001": { "01": .2, "10": .2, "00": .4, "11": .2 },
        "1001": { "00": .5, "01": .5 },
        "0011": { "11": .3, "01": .6, "00": .1 }
    }
