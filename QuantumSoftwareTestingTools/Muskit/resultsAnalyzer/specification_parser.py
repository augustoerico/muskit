"""
Module to parse the Quantum Program specification into a dictionary
"""
from pathlib import Path
from typing import List, Tuple

def parse(specification_file_path: Path):
    """
    parses the Quantum Program specification file into a dictionary
    """
    output_probabilities_by_input = {}
    with open(specification_file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            input_value, output, probability = \
                parse_specification_line(line)
            output_probabilities_by_input = \
                add_to_output_probabilities_by_input_dict(
                    input_value, output, probability,
                    output_probabilities_by_input
                    )
    return fix_number_of_bits(output_probabilities_by_input)

def fix_number_of_bits(output_probabilities_by_input: dict):
    """
    add zeros to the left to match the highest bit counts
    """
    max_lenght_of_bits = 0
    for i in output_probabilities_by_input.keys():
        lenght_of_bits = len(i)
        if lenght_of_bits > max_lenght_of_bits:
            max_lenght_of_bits = lenght_of_bits
    result = {}
    for i, op in output_probabilities_by_input.items():
        result[i.zfill(max_lenght_of_bits)] = {
            o.zfill(max_lenght_of_bits): p
            for o, p in op.items()
        }
    return result

def parse_specification_line(line: str) -> Tuple[str, str, float]:
    """
    parse the Quantum Program specification file line into a tuple
        input, output, probability
    """
    return *extract_input_output_pair(line), extract_probability(line)

def extract_input_output_pair(line: str) -> List[str]:
    """
    extracts the (input, output) pair from the specification line
    """
    input_output_pair = line[
        line.find('(') + 1:line.find(')')
        ]
    input_str, output_str = input_output_pair.split(',')
    input_value = int(input_str.strip())
    output = int(output_str.strip())
    return [format(input_value, 'b'), format(output, 'b')]

def extract_probability(line: str) -> float:
    """
    extracts the probability from the specification line
    """
    probability_str = line.split(':')[1]
    return float(probability_str.strip())

def add_to_output_probabilities_by_input_dict(
        input_value: str, output: str, probability: float,
        counts_by_input: dict) -> dict:
    """
    adds outputs and respective probabilities into the
        output_probabilities_by_input dictionary
    """
    if input_value in counts_by_input:
        # concatenate dictionaries
        counts_by_input[input_value] = {
            **counts_by_input[input_value],
            output: probability
        }
    else:
        # create entry in dictionary
        counts_by_input[input_value] = {
            output: probability
        }
    return counts_by_input
