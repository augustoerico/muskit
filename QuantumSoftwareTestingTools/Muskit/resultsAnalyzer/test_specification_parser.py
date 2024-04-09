"""
Tests for the specification_parser module
"""
from specification_parser import get_len_qubits_in_output, \
    get_len_qubits_in_input, fix_number_of_qubits, \
        get_output_probabilities_by_input_from_file_lines

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

def test_should_parse_the_spec_lines_into_json():
    """
    test_should_parse_the_spec_lines_into_json
    """
    # given
    spec_lines = [
        "(0, 1): 1.0", "(1, 1): 1.0", "(2, 1): 0.25", "(2, 2): 0.75",
        "(3, 1): 0.75", "(3, 2): 0.25", "(4, 1): 0.25", "(4, 3): 0.75",
        "(5, 1): 0.75", "(5, 3): 0.25", "(6, 0): 0.75", "(6, 1): 0.25",
        "(7, 0): 0.25", "(7, 1): 0.75"
    ]

    # when
    result = get_output_probabilities_by_input_from_file_lines(spec_lines)

    # then
    assert result == {
        "0": { "1": 1. }, "1": { "1": 1. }, "10": { "1": .25, "10": .75 },
        "11": { "1": .75, "10": .25 }, "100": { "1": .25, "11": .75 },
        "101": { "1": .75, "11": .25 }, "110": { "0": .75, "1": .25 },
        "111": { "0": .25, "1": .75 }
    }
