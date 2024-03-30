"""
Muskit entry point
"""
import os
from pathlib import Path

from rich.console import Console
import toml
import typer
from typing_extensions import Annotated

from functionalities import createMutants as create_mutants

app = typer.Typer()

typer_options = { "exists": True, "readable": True, "resolve_path": True }
error_console = Console(stderr=True)

@app.command()
def create(
    config: Annotated[Path, typer.Option(**typer_options)],
    circuit: Annotated[Path, typer.Option(**typer_options)]
    ):
    """
    create mutants
    """
    config_options = toml.load(config)
    circuit_file_path = circuit.absolute()
    try:
        create_mutants(
            config_options.get('max_number_of_mutants'),
            config_options.get('operators'),
            config_options.get('types'),
            config_options.get('gate_number'),
            config_options.get('location'),
            str(circuit_file_path),
            str(os.path.dirname(circuit_file_path)),
            config_options.get('all_mutants'),
            config_options.get('phases')
        )
    except FileExistsError as e:
        error_console.print(e, style="red")
        raise typer.Abort()

@app.command()
def execute(
    config: Annotated[Path, typer.Option(**typer_options)],
    test_cases: Annotated[Path, typer.Option(**typer_options)],
    circuit: Annotated[Path, typer.Option(**typer_options)]
    ):
    """
    execute mutants
    """
    # python Muskit/CommandMain.py Execute Muskit/executorConfig.py Muskit/testCases.py Example/AddMutations/10AddGate_ry_inGap_1_.py
    print(f'opens: {config}')
    print(f'opens: {test_cases}')
    print(f'opens: {circuit}')
    print('executing mutants')

if __name__ == '__main__':
    app()
