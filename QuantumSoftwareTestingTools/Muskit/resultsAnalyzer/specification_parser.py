"""
Module to parse the Quantum Program specification into a dictionary
"""
from os.path import dirname, basename
from pathlib import Path
from typing import List, Tuple

import simplejson

def parse(specification_file_path: Path, save_output: bool = True):
    """
    parses the Quantum Program specification file into a dictionary
    """
    # [TODO] extract the file read and save to a higher level
    # then add a test
    with open(specification_file_path, 'r', encoding='utf-8') as file:
        output_probabilities_by_input = \
            get_output_probabilities_by_input_from_file_lines(file.readlines())

    parsed = fix_number_of_qubits(output_probabilities_by_input)
    if save_output:
        save_parsed_spec(specification_file_path, parsed)
    return parsed

def get_output_probabilities_by_input_from_file_lines(lines: List[str]) -> dict:
    """
    get_output_probabilities_by_input_from_file_lines
    """
    output_probabilities_by_input = {}
    for line in lines:
        input_value, output, probability = parse_specification_line(line)
        if input_value not in output_probabilities_by_input:
            output_probabilities_by_input[input_value] = { output: probability }
        else:
            outputs = output_probabilities_by_input[input_value]
            output_probabilities_by_input[input_value] = { **outputs, output: probability}
    return output_probabilities_by_input

def save_parsed_spec(specification_file_path: Path, output_probabilities_by_input: dict):
    """
    saves the output_probabilities_by_input dict into a JSON object
    """
    dir_name = dirname(specification_file_path)
    file_name = basename(specification_file_path).split('.', 1)[0]
    json_file_path = f"{dir_name}/{file_name}.spec.json"
    with open(json_file_path, 'w', encoding='utf-8') as file:
        simplejson.dump(output_probabilities_by_input, fp=file, indent=4)

def fix_number_of_qubits(outputs_probabilities_by_input: dict) -> dict:
    """
    add zeros to the left to match input and output qubit counts
        separately
    """
    inputs = outputs_probabilities_by_input.keys()
    max_n_qubits_input = get_len_qubits_in_input(inputs)

    outputs_probabilities = outputs_probabilities_by_input.values()
    max_n_qubits_output = get_len_qubits_in_output(outputs_probabilities)

    result = {}
    for input_value, outputs_probabilities in \
        outputs_probabilities_by_input.items():
        result[input_value.zfill(max_n_qubits_input)] = {
            output.zfill(max_n_qubits_output): probability
            for output, probability in \
            outputs_probabilities.items()
            }
        
    return result

def get_len_qubits_in_output(
        outputs_probabilities: List[dict]) -> int:
    """
    get_len_qubits_in_output
    """
    max_len_qubits = 0
    for i in outputs_probabilities:
        for output in i.keys():
            len_qubits = len(output)
            if len_qubits > max_len_qubits:
                max_len_qubits = len_qubits
    return max_len_qubits

def get_len_qubits_in_input(inputs: List[str]) -> int:
    """
    get_len_qubits_in_input
    """
    max_len_qubits = 0
    for i in inputs:
        len_qubits = len(i)
        if len_qubits > max_len_qubits:
            max_len_qubits = len_qubits
    return max_len_qubits

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
