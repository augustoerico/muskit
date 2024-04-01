"""
Main app tests
"""
import pytest
from typer.testing import CliRunner

from main import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    changes the working dir to this one
    """
    monkeypatch.chdir(request.fspath.dirname)

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

def test_should_execute_mutants_with_default_inputs():
    """
    test should execute mutants with default inputs
        without raising an exception
    """

    # given
    args = ["execute",
            "--config", "configs/default.execute.toml",
            "--test-cases", "configs/test.inputs.toml",
            "../ExampleTest/1AddGate_x_inGap_1_.py",
            "../ExampleTest/1ReplaceGate.py",
            "../ExampleTest/RemoveGate_1_.py"]

    # when
    result = runner.invoke(app, args)

    # then
    assert result.exit_code == 0
