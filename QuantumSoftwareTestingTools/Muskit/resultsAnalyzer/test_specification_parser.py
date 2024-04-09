"""
Tests for the specification_parser module
"""
from specification_parser import get_output_probabilities_by_input_from_file_lines

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
