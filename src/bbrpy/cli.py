import pathlib
import webbrowser

import rich
import typer
from rich.markup import escape

from .exceptions import PlatformError
from .models import BatteryReport
from .version import __version__

app = typer.Typer()


def _get_battery_report() -> BatteryReport:
    """Generates the battery report and handles PlatformError."""
    try:
        return BatteryReport.generate()
    except PlatformError as e:
        rich.print(f":warning:  [bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


def _display_version(value: bool) -> None:
    """Display the version of the application and exit."""
    if value:
        typer.echo(f"bbrpy {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_display_version,
        help="Display the version and exit.",
        is_eager=True,  # Process version before other logic
    ),
):
    """Handle version and ensure battery report is available."""
    # Generate and store the report object in the context
    ctx.obj = _get_battery_report()


@app.command()
def info(ctx: typer.Context):
    """Display basic battery information from the latest report."""
    report: BatteryReport = ctx.obj  # Get the report from the context
    rich.print(f":alarm_clock: Scan Time: [green]{report.scan_time}[/green]")
    rich.print(f":battery: Capacity Status: {report.full_cap}/{report.design_cap} mWh")


@app.command()
def report(
    ctx: typer.Context,
    output: str = "./reports/battery_report.html",
):
    """Generate a battery report with capacity history visualization."""

    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        rich.print(
            ":warning:  [bold red]Error: [/bold red] Missing extra dependencies!\n"
            f"Use [yellow]{escape('bbrpy[report]')}[/yellow] to run this command"
        )
        raise typer.Exit(1)

    # Generate the battery report and extract the capacity history
    report: BatteryReport = ctx.obj  # Get the report from the context
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
