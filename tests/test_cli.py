import re

from typer.testing import CliRunner

from bbrpy.cli import app

runner = CliRunner()


def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert re.match(r"bbrpy version \d+\.\d+\.\d+", result.stdout)


def test_app_version_short():
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert re.match(r"bbrpy version \d+\.\d+\.\d+", result.stdout)
