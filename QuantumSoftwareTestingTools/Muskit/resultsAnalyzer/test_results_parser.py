"""
Tests for the results_parser module
"""
from pathlib import Path
import pytest
import results_parser

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    changes the working dir to this one
    """
    monkeypatch.chdir(request.fspath.dirname)

def test_should_extract_mutant_file_path_from_results_line():
    """
    test should extract the mutant file path from a valid results line
    """
    # given
    line = "The result of E:\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExampleTest" \
        + "\\1AddGate_x_inGap_1_.py with input [0000001] is: {'0001101': 69, '0001001': 31}"

    # when
    mutant_file_path = results_parser.extract_mutant_path(line)

    # then
    assert mutant_file_path == \
        "E:\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExampleTest\\1AddGate_x_inGap_1_.py"

def test_should_extract_counts_by_input_from_results_line():
    """
    test should extract the counts by input dictionary from a valid results line
    """
    # given
    line = "The result of E:\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExampleTest" \
        + "\\1AddGate_x_inGap_1_.py with input [0000001] is: {'0001101': 69, '0001001': 31}"

    # when
    counts_by_input = results_parser.extract_counts_by_input(line)

    # then
    assert counts_by_input == { '0000001': { '0001101': 69, '0001001': 31 } }

def test_should_extract_counts_by_input_from_results_line_with_n_qubits():
    """
    test_should_extract_counts_by_input_from_results_line_with_n_qubits
    """
    # given
    line = "The result of E:\\muskit\\QuantumSoftwareTestingTools\\Muskit\\ExampleTest" \
        + "\\1AddGate_x_inGap_1_.py with input [0000001] is: {'0001101': 69, '0001001': 31}"
    n_qubits = 4

    # when
    counts_by_input = results_parser.extract_counts_by_input(line, n_qubits)

    # then
    assert counts_by_input == { '0001': { '1101': 69, '1001': 31 } }

def test_should_add_counts_by_id_into_an_empty_output_dictionary():
    """
    test should add counts by id dictionary into an empty output dictionary
    """
    # given
    mutant_path = "/some/valid/path/mutant.py"
    counts_by_input = { '0000001': { '0001101': 69, '0001001': 31 } }
    output = {}

    # when
    output = results_parser.add_counts_by_input(
        mutant_path, counts_by_input, output)

    # then
    assert output == {
        '/some/valid/path/mutant.py': {
            '0000001': { '0001101': 69, '0001001': 31 }
        }
    }

def test_should_add_counts_by_id_into_a_non_empty_dictionary_1():
    """
    test should add counts by id dictionary into a dictionary that already
        contains some data for the same mutant path
    """
    # given
    mutant_path = "/some/valid/path/mutant.py"
    counts_by_input = { '0000001': { '0001101': 69, '0001001': 31 } }
    output = { "/some/valid/path/mutant.py": {
        '0000101': { '0001001': 76, '0001101': 24 }
    } }

    # when
    output = results_parser.add_counts_by_input(
        mutant_path, counts_by_input, output)

    # then
    assert output == {
        '/some/valid/path/mutant.py': {
            '0000001': { '0001101': 69, '0001001': 31 },
            '0000101': { '0001001': 76, '0001101': 24 }
        }
    }

def test_should_add_counts_by_id_into_a_non_empty_dictionary_2():
    """
    test should add counts by id dictionary into a dictionary that already
        contains some data for the a different mutant
    """
    # given
    mutant_path = "/differente/valid/path/mutant_2.py"
    counts_by_input = { '0000001': { '0001101': 69, '0001001': 31 } }
    output = { "/some/valid/path/mutant.py": {
        '0000101': { '0001001': 76, '0001101': 24 }
    } }

    # when
    output = results_parser.add_counts_by_input(
        mutant_path, counts_by_input, output)

    # then
    assert output == {
        '/some/valid/path/mutant.py': {
            '0000101': { '0001001': 76, '0001101': 24 }
        },
        '/differente/valid/path/mutant_2.py': {
            '0000001': { '0001101': 69, '0001001': 31 },
        }
    }

def test_should_break_results_file_into_smaller_sections():
    """
    test should break a results file into sections based on the mutant path
    """
    # given
    results_file_path = "test_resources/example_results.txt"

    # when
    counts_by_mutant_by_inputs = results_parser \
        .break_results_into_smaller_sections(results_file_path)

    # then
    assert counts_by_mutant_by_inputs == {
        "/some/valid/path/test_example/1AddGate_x_inGap_1_.py": {
            '0000001': { '0001101': 69, '0001001': 31 },
            '0000101': { '0001001': 76, '0001101': 24 },
            '0000110': { '0010001': 78, '0010101': 22 }
        },
        "/some/valid/path/test_example/RemoveGate_1_.py": {
            '0000001': { '0001101': 52, '0001001': 48 },
            '0000101': { '0001001': 48, '0001101': 52 },
            '0000110': { '0010101': 47, '0010001': 53 }
        },
        "/some/valid/path/test_example/1ReplaceGate.py": {
            '0000001': { '0001101': 58, '0001001': 42 },
            '0000101': { '0001101': 50, '0001001': 50 },
            '0000110': { '0010001': 49, '0010101': 51 }
        }
    }

def test_should_parse_results_file_into_json_files():
    """
    test should parse a valid results file into multiple results json files,
        one for each mutant
    """
    # given
    results_file_path = "test_resources/example_results.txt"

    # when
    results_parser.parse(results_file_path)

    # then
    # assert no exception was raised during the process
    #   and manually check test_resources/results_json folder
    # [TODO] make better assertions
    assert True

def test_should_parse_results_into_json_files_given_the_output_dir():
    """
    test should parse a valid results file into multiple results json files,
        one for each mutant, in the specified output dir `my_dir`
    """
    # given
    results_file_path = Path("test_resources/example_results.txt")
    n_qubits = None # do not define the qubits length
    output_dir = Path("test_resources/my_dir/my_sub_dir")

    # when
    results_parser.parse(
        results_file_path,
        n_qubits=n_qubits,
        output_dir=output_dir)

    # then
    # assert no exception was raised during the process
    #   and manually check test_resources/my_dir/results_json folder
    # [TODO] make better assertions
    assert True
