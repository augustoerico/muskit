"""
Tests for op_oracle module
"""
from op_oracle import add_zero_count_for_non_observed_outputs

def test_should_add_zero_count_for_non_observed_outputs():
    """
    test should add zero count for non observed outputs that
        are expected
    """
    # given
    observed_outputs_counts = { # "01" not observed
        "00": 15, "10": 6, "11": 29
    }
    expected_outputs_probabilities = {
        "00": .1478, "01": .5505, "10": .0675, "11": .2342
    }

    # when
    observed_outputs_counts_result = \
        add_zero_count_for_non_observed_outputs(
            observed_outputs_counts,
            expected_outputs_probabilities)

    # then
    assert observed_outputs_counts_result == {
        "00": 15, "01": 0, "10": 6, "11": 29
    }

def test_should_not_change_counts_if_all_expected_outputs_are_observed():
    """
    test should not change counts if all expected outputs are observed
    """
    # given
    observed_outputs_counts = {
        "00": 15, "01": 55, "10": 6, "11": 29
    }
    expected_outputs_probabilities = {
        "00": .1478, "01": .5505, "10": .0675, "11": .2342
    }

    # when
    observed_outputs_counts_result = \
        add_zero_count_for_non_observed_outputs(
            observed_outputs_counts,
            expected_outputs_probabilities)

    # then
    assert observed_outputs_counts_result == {
        "00": 15, "01": 55, "10": 6, "11": 29
    }

def test_should_add_zero_count_when_probability_expected_is_zero():
    """
    test should add zero count when probability is also zero
    """
    # given
    observed_outputs_counts = {
        "00": 15, "01": 55, "11": 29
    }
    expected_outputs_probabilities = {
        "00": .2153, "01": .5505, "10": .0, "11": .2342
    }

    # when
    observed_outputs_counts_result = \
        add_zero_count_for_non_observed_outputs(
            observed_outputs_counts,
            expected_outputs_probabilities)

    # then
    assert observed_outputs_counts_result == {
        "00": 15, "01": 55, "10": 0, "11": 29
    }
