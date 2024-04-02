"""
Module to parse results file produced by Muskit.execute
"""
import ast
from pathlib import Path


def parse(file_path: Path) -> None:
    """
    parse results file
    """
    break_results_into_smaller_sections(file_path)

def break_results_into_smaller_sections(file_path: Path) -> dict:
    """
    breaks the results.txt file into smaller sections corresponding
        to each mutant circuit
    """
    counts_by_mutant_by_input = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            mutant_path, counts_by_input = \
                extract_mutant_path(line) \
                , extract_counts_by_input(line)
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

def extract_counts_by_input(line: str) -> dict:
    """
    extracts the output counts from results line
    """
    input_start, input_end = line.find("["), line.find("]")
    input_value = line[input_start + 1:input_end]
    counts_start, counts_end = line.find("{"), line.find("}")
    counts = ast.literal_eval(line[counts_start: counts_end + 1])
    return { input_value: counts }
  