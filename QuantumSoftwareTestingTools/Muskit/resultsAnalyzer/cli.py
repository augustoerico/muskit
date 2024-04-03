"""
CLI entry for analysing results
"""
from pathlib import Path

import typer
from typing_extensions import Annotated
from rich.console import Console

from results_parser import parse as r_parse
from specification_parser import parse as s_parse

app = typer.Typer()

typer_options = { "exists": True, "readable": True, "resolve_path": True }
fail_console = Console(stderr=True)
pass_console = Console()


@app.command()
def parse_results(results: Annotated[Path, typer.Option(**typer_options)]):
    """
    parse results from Muskit.execute into multiple json files
    """
    r_parse(results)

@app.command()
def parse_spec(spec: Annotated[Path, typer.Option(**typer_options)]):
    """
    parses a specification into JSON format
    """
    s_parse(spec)

# @app.command()
# def verify_woo(
#     results: Annotated[Path, typer.Option(**typer_options)],
#     specification: Annotated[Path, typer.Option(**typer_options)]
#     ):
#     """
#     Verify results obtained from Muskit.execute against the program specification.
#         It also creates JSON files for each mutant execution
#     """
#     try:
#         # assert_all_valid_outputs()
#         message = "PASS"
#         pass_console.print(message, style="green")
#     except AssertionError as _:
#         message = "FAIL"
#         fail_console.print(message, style="red")


if __name__ == '__main__':
    app()
