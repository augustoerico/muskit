"""
Main app tests
"""
from typer.testing import CliRunner

from main import app

runner = CliRunner()

def test_should_create_mutants_with_default_inputs():
    """
    test should create mutants with default inputs
        without raising an exception
    """
    # given
    args = ["create",
            "--config", "configs/default.create.toml",
            "--circuit", "../Example/QRAM_program.py"]
    
    # when
    result = runner.invoke(app, args)

    # then
    assert result.exit_code == 0
