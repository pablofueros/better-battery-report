from typer.testing import CliRunner

from bbrpy.cli import app

runner = CliRunner()


def test_app_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Computer Name" in result.stdout
    assert "Scan Time" in result.stdout
    assert "Design Capacity" in result.stdout
    assert "Full Charge Capacity" in result.stdout
