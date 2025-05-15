import pathlib
import webbrowser

import rich
import typer
from rich.markup import escape

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
    report = BatteryReport.generate()
    rich.print(f":alarm_clock: Scan Time: [green]{report.scan_time}[/green]")
    rich.print(f":battery: Capacity Status: {report.full_cap}/{report.design_cap} mWh")


@app.command()
def report(
    output: str = "./reports/battery_report.html",
):
    """Generate a battery report with capacity history visualization."""

    # Check if the required libraries are installed
    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        rich.print(
            ":warning: [red]Error: Missing extra dependencies![/red]\n"
            f"Please, use [yellow]{escape('bbrpy[report]')}[/yellow] to run this command."
        )
        raise typer.Exit(1)

    # Generate the battery report and extract the capacity history
    report = BatteryReport.generate()
    history_df = pd.DataFrame([entry.model_dump() for entry in report.History])

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
    rich.print(f"Report generated successfully in [blue]{directory}[/blue]")

    # Open the report in the default browser
    webbrowser.open(f"file://{output_path}")


if __name__ == "__main__":
    app()
