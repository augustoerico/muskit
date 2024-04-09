"""
Tests for op_oracle module
"""
from op_oracle import add_zero_count_for_non_observed_outputs, \
    add_zero_count_for_non_observed_outputs_by_input, \
    add_zero_probability_for_non_expected_outputs, \
    add_zero_probability_for_non_expected_outputs_by_input, \
    get_expected_outputs_counts, \
    get_expected_outputs_counts_by_input

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

def test_should_add_zero_counts_for_all_non_observed_outputs_by_input():
    """
    test should add zero counts for all non observed outputs to the dict
        containing the output counts for each input
    """
    # given
    observed_outputs_counts_by_input = {
        "00": { "00": 15, "10": 6, "11": 29 },
        "01": { "00": 16, "01": 55, "11": 19 },
        "10": { "00": 2, "01": 60, "10": 10, "11": 11 },
        "11": { "00": 11, "01": 2, "10": 60, "11": 10 }
    }
    expected_outputs_probabilities_by_input = {
        "00": { "00": .1478, "01": .5505, "10": .0675, "11": .2342 },
        "01": { "00": .165, "01": .555, "10": .0, "11": .28 },
        "10": { "00": .3, "01": .2, "10": .25, "11": .25},
        "11": { "00": .09, "01": .21, "10": .4, "11": .3 }
    }

    # when
    observed_outputs_counts_result = \
        add_zero_count_for_non_observed_outputs_by_input(
            observed_outputs_counts_by_input,
            expected_outputs_probabilities_by_input)

    # then
    assert observed_outputs_counts_result == {
        "00": { "00": 15, "01": 0, "10": 6, "11": 29 },
        "01": { "00": 16, "01": 55, "10": 0, "11": 19 },
        "10": { "00": 2, "01": 60, "10": 10, "11": 11 },
        "11": { "00": 11, "01": 2, "10": 60, "11": 10 }
    }

def test_should_add_zero_probability_for_non_expected_outputs():
    """
    test_should_add_zero_probability_for_non_expected_outputs
    """
    # given
    expected_outputs_probabilities = {
        "00": .5, "10": .2, "11": .3    # "01" is not expected
    }
    observed_outputs_counts = {
        "00": 42, "01": 3, "10": 10, "11": 15
    }

    # when
    result = add_zero_probability_for_non_expected_outputs(
        expected_outputs_probabilities,
        observed_outputs_counts
        )
    
    # then
    assert result == {
        "00": .5, "01": .0, "10": .2, "11": .3
    }

def test_should_not_change_probabilities_it_all_observed_outputs_are_expected():
    """
    test_should_not_change_probabilities_it_all_observed_outputs_are_expected
    """
    # given
    expected_outputs_probabilities = {
        "00": .5, "01": .1, "10": .2, "11": .2
    }
    observed_outputs_counts = {
        "00": 7, "01": 0, "10": 2, "11": 1
    }

    # when
    result = add_zero_probability_for_non_expected_outputs(
        expected_outputs_probabilities,
        observed_outputs_counts)
    
    # then
    assert result == {
        "00": .5, "01": .1, "10": .2, "11": .2
    }

def test_should_add_zero_probabilities_for_non_expected_outputs_by_input():
    """
    test_should_add_zero_probabilities_for_non_expected_outputs_by_input
    """
    # given
    expected_outputs_probabilities_by_input = {
        "00": { "00": .5, "01": .1, "10": .4 },
        "01": { "01": .3, "10": .4, "11": .3 },
        "10": { "00": .3, "01": .2, "10": .25, "11": .25},
        "11": { "00": .09, "01": .21, "10": .0, "11": .7 }
    }
    observed_outputs_counts_by_input = {
        "00": { "00": 15, "01": 2, "10": 6, "11": 29 },
        "01": { "01": 55, "10": 23, "11": 19 }, # "00" was neither observer, nor expected
        "10": { "00": 2, "01": 60, "10": 10 }, # "11" was not observed, but it is expected
        "11": { "00": 11, "01": 2, "10": 60, "11": 10 }
    }
    

    # when
    result = \
        add_zero_probability_for_non_expected_outputs_by_input(
            expected_outputs_probabilities_by_input,
            observed_outputs_counts_by_input)

    # then
    assert result == {
        "00": { "00": .5, "01": .1, "10": .4, "11": .0 },
        "01": { "01": .3, "10": .4, "11": .3 },
        "10": { "00": .3, "01": .2, "10": .25, "11": .25 },
        "11": { "00": .09, "01": .21, "10": .0, "11": .7 }
    }

def test_should_get_expected_output_counts():
    """
    test_should_get_expected_output_counts
    """
    # given
    expected_outputs_probabilities = {
        "00": .1478, "01": .5505, "10": .0675, "11": .2342
    }
    total_observed_counts = 1000

    # when
    expected_outputs_counts = get_expected_outputs_counts(
        expected_outputs_probabilities,
        total_observed_counts)

    # then
    assert expected_outputs_counts == {
        "00": 148, "01": 550, "10": 68, "11": 234
    }

def test_should_get_expected_output_counts_with_zero_probability():
    """
    test_should_get_expected_output_counts_with_zero_probability
    """
    # given
    expected_outputs_probabilities = {
        "00": .1478, "01": .618, "10": .0, "11": .2342
    }
    total_observed_counts = 1000

    # when
    expected_outputs_counts = get_expected_outputs_counts(
        expected_outputs_probabilities,
        total_observed_counts)

    # then
    assert expected_outputs_counts == {
        "00": 148, "01": 618, "10": 0, "11": 234
    }

def test_should_get_expected_output_counts_by_input():
    """
    test_should_get_expected_output_counts_by_input
    """
    # given
    expected_outputs_probabilities_by_input = {
        "00": { "00": .1478, "01": .5505, "10": .0675, "11": .2342 },
        "01": { "00": .165, "01": .555, "10": .0, "11": .28 },
        "10": { "00": .3, "01": .2, "10": .25, "11": .25},
        "11": { "00": .09, "01": .21, "10": .4, "11": .3 }
    }
    total_observed_counts_by_input = {
        "00": 50, "01": 90, "10": 84, "11": 84
    }

    # when
    expected_output_counts_by_input = \
        get_expected_outputs_counts_by_input(
            expected_outputs_probabilities_by_input,
            total_observed_counts_by_input
            )

    # then
    assert expected_output_counts_by_input == {
        "00": { "00": 7, "01": 28, "10": 3, "11": 12 },
        "01": { "00": 15, "01": 50, "10": 0, "11": 25 },
        "10": { "00": 25, "01": 17, "10": 21, "11": 21},
        "11": { "00": 8, "01": 18, "10": 34, "11": 25 }
    }
