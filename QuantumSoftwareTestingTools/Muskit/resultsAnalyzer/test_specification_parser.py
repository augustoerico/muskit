"""
Tests for the specification_parser module
"""
import pytest
import specification_parser

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    changes the working dir to this one
    """
    monkeypatch.chdir(request.fspath.dirname)

def test_should_parse_the_specification_file():
    """
    test should parse the valid example specification file
        into a dictionary with the output probabilities by
        input
    """
    # given
    specification_file_path = "test_resources/qram.spec.txt"

    # when
    output_probabilities_by_input = \
        specification_parser.parse(specification_file_path)
    print(output_probabilities_by_input)

    # then
    assert output_probabilities_by_input == {
        '000': { '001': 1.0 },
        '001': { '001': 1.0 },
        '010': { '001': 0.24999999999999994,
                  '010': 0.7500000000000001 },
        '011': { '001': 0.7500000000000001,
                  '010': 0.2499999999999999 },
        '100': { '001':0.24999999999999994 ,
                  '011': 0.7500000000000001 },
        '101': { '001': 0.7500000000000001,
                  '011': 0.2499999999999999 },
        '110': { '000': 0.7500000000000001,
                  '001': 0.24999999999999994 },
        '111': { '000': 0.2499999999999999,
                  '001': 0.7500000000000001 }
    }
