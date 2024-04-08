"""
Module to parse results file produced by Muskit.execute
"""
import ast
import json
from os import mkdir
from os.path import basename, dirname, exists
from pathlib import Path
from typing_extensions import Optional


def parse(file_path: Path, n_qubits: Optional[int] = None) -> None:
    """
    parse results file into json data
    """
    json_dump_options = { 'sort_keys': True, 'indent': 4 }

    counts_by_mutant_by_input = \
        break_results_into_smaller_sections(file_path, n_qubits)

    output_dir = f"{dirname(file_path)}/json_results"
    if not exists(output_dir):
        mkdir(output_dir)

    for mutant_file_path, counts_by_input in counts_by_mutant_by_input.items():
        results_file_name = str(basename(mutant_file_path)) \
            .split('.', maxsplit=1)[0] # mutant file name without '.py' extension
        with open(
            f"{output_dir}/{results_file_name}.json",
            'w+', encoding='utf-8') as file:
            json.dump(counts_by_input, fp=file, **json_dump_options)

def break_results_into_smaller_sections(file_path: Path, n_qubits: Optional[int] = None) -> dict:
    """
    breaks the results.txt file into smaller sections corresponding
        to each mutant circuit
    """
    counts_by_mutant_by_input = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            mutant_path, counts_by_input = \
                extract_mutant_path(line) \
                , extract_counts_by_input(line, n_qubits)
            counts_by_mutant_by_input = add_counts_by_input(
                mutant_path, counts_by_input, counts_by_mutant_by_input
                )
    return counts_by_mutant_by_input

def add_counts_by_input(mutant_path: str, counts_by_input: dict,
                        counts_by_mutant_by_input: dict) -> dict:
    """
    adds counts by input dictionary into the mutation dictionary
    """
    if mutant_path in counts_by_mutant_by_input:
        # concatenate dictionaries
        counts_by_mutant_by_input[mutant_path] = {
            **counts_by_mutant_by_input[mutant_path],
            **counts_by_input
        }
    else:
        # create entry in dictionary
        counts_by_mutant_by_input[mutant_path] = \
            counts_by_input
    return counts_by_mutant_by_input

def extract_mutant_path(line: str) -> str:
    """
    extracts mutant file path
    """
    prefix = "The result of "
    suffix = " with input "
    i_suffix = line.find(suffix)
    return line[len(prefix):i_suffix]

def extract_counts_by_input(line: str, n_qubits: Optional[int] = None) -> dict:
    """
    extracts the output counts from results line
    """
    input_start, input_end = line.find("[") + 1, line.find("]")
    input_n_qubits = input_end - input_start
    if n_qubits and input_n_qubits > n_qubits:
        input_start = input_end - n_qubits
    input_value = line[input_start:input_end]
    counts = extract_counts_dict(line, n_qubits)
    return { input_value: counts }

def extract_counts_dict(line: str, n_qubits: Optional[int] = None) -> dict:
    """
    extract_counts_dict
    """
    counts_start, counts_end = line.find("{"), line.find("}") + 1
    counts = ast.literal_eval(line[counts_start:counts_end])
    if n_qubits is not None:
        result = {}
        for output, c in counts.items():
            if len(output) > n_qubits:
                output = output[-n_qubits:]
            result[output] = c
        return result
    return counts
