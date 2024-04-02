"""
CLI entry for analysing results
"""
from pathlib import Path

import typer
from typing_extensions import Annotated
from rich.console import Console

from results_parser import parse

app = typer.Typer()

typer_options = { "exists": True, "readable": True, "resolve_path": True }
error_console = Console(stderr=True)

@app.command()
def parse_results(results_file_path: Annotated[Path, typer.Option(**typer_options)]):
    """
    parse results from Muskit.execute into multiple json files
    """
    parse(results_file_path)

if __name__ == '__main__':
    app()
