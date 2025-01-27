import pathlib
import webbrowser

import plotly.express as px
import polars as pl
import typer

from .models import BatteryReport
from .version import __version__

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"bbrpy version {__version__}\n")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Display the version and exit.",
    ),
):
    pass


@app.command()
def info():
    """Display basic battery information from the latest report."""
    battery_report = BatteryReport.generate()
    typer.echo(f"Computer Name: {battery_report.computer_name}")
    typer.echo(f"Scan Time: {battery_report.scan_time}")
    typer.echo(f"Design Capacity: {battery_report.design_cap} mWh")
    typer.echo(f"Full Charge Capacity: {battery_report.full_cap} mWh")


@app.command()
def generate(
    output: str = "./reports/battery_report.html",
):
    """Generate a battery report with capacity history visualization."""

    # Generate the battery report and extract the capacity history
    battery_report = BatteryReport.generate()
    history_df = pl.DataFrame([entry.model_dump() for entry in battery_report.History])

    # Generate the capacity history visualization
    fig = px.line(
        history_df,
        x="StartDate",
        y=["DesignCapacity", "FullChargeCapacity"],
        labels={"value": "Capacity (mWh)", "variable": "Type"},
        title="Battery Capacity Over Time",
        template="plotly_dark",
    )

    # Create the output directory if it does not exist
    output_path = pathlib.Path(output).resolve()
    directory = output_path.parent
    directory.mkdir(parents=True, exist_ok=True)

    # Save the report to an HTML file
    fig.write_html(output_path.with_suffix(".html"))
    styled_dir = typer.style(str(directory), fg=typer.colors.BLUE)
    typer.echo(f"Report generated successfully in {styled_dir}")

    # Open the report in the default browser
    webbrowser.open(f"file://{output_path}")


if __name__ == "__main__":
    app()
