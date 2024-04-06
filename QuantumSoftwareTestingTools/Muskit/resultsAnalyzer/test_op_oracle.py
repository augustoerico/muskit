"""
Tests for op_oracle module
"""
from op_oracle import get_total_observed_output_counts, \
    get_total_expected_output_counts

def test_should_get_total_observed_output_counts():
    """
    test should get the total observed output given
        the observed outputs by input
    """
    # given
    observed_outputs_by_input = {
        "0000000": { "0000001": 24, "0000101": 76 },
        "0000001": { "0001001": 29, "0001101": 71 },
        "0000010": { "0010001": 29, "0010101": 71 },
        "0000011": { "0011001": 29, "0011101": 71 },
        "0000100": { "0000001": 75, "0000101": 25 },
        "0000101": { "0001001": 73, "0001101": 27 },
        "0000110": { "0010001": 75, "0010101": 25 },
        "0000111": { "0011001": 79, "0011101": 21 }
    }

    # when
    counts, total = get_total_observed_output_counts(
        observed_outputs_by_input)

    # then
    assert total == 800
    assert counts == {
        "0000001": 99, "0000101": 101,
        "0001001": 102, "0001101": 98,
        "0010001": 104, "0010101": 96,
        "0011001": 108, "0011101": 92
    }

def test_should_get_total_expected_output_counts():
    """
    test should get the total expected output counts given
        the expected output probabilities and the total
        observed count
    """
    # given
    total = 1600
    expected_outputs_by_input = {
        "0000000": { "0000001": 1.0 },
        "0000001": { "0000001": 1.0 },
        "0000010": { "0000001": 0.25, "0000010": 0.75 },
        "0000011": { "0000001": 0.75, "0000010": 0.25 },
        "0000100": { "0000001": 0.25, "0000011": 0.75 },
        "0000101": { "0000001": 0.75, "0000011": 0.25 },
        "0000110": { "0000000": 0.75, "0000001": 0.25 },
        "0000111": { "0000000": 0.25, "0000001": 0.75 },
    }

    # when
    counts = get_total_expected_output_counts(
        expected_outputs_by_input, total)

    # then
    assert counts == {
        "0000000": 200, "0000001": 1000,
        "0000010": 200, "0000011": 200,
    }
