import pathlib
import webbrowser

import rich
import typer
from rich.markup import escape

from .exceptions import PlatformError
from .generator import generate_battery_report_html, generate_battery_report_xml
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
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_display_version,
        help="Display the version and exit.",
        is_eager=True,  # Process version before other logic
    ),
):
    pass


@app.command()
def info():
    """Display basic battery information from the latest report."""
    report: BatteryReport = _get_battery_report()
    rich.print(f":alarm_clock: Scan Time: [green]{report.scan_time}[/green]")
    rich.print(f":battery: Capacity Status: {report.full_cap}/{report.design_cap} mWh")


@app.command()
def report(
    output: str = typer.Option(
        "./reports/battery_report",
        "--output",
        "-o",
        help="Output directory for the report",
    ),
    format: str = typer.Option(
        "better",
        "--format",
        "-f",
        help="Report format: 'better' (custom html), 'default' (Windows html), or 'raw' (xml data)",
    ),
):
    """Generate a battery report in various formats."""

    # Create the output directory if it doesn't exist
    output_path = pathlib.Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == "better":
        # Generate interactive plotly visualization
        try:
            import pandas as pd
            import plotly.express as px
        except ImportError:
            rich.print(
                ":warning:  [bold red]Error: [/bold red] Missing extra dependencies!\n"
                f"Use [yellow]{escape('bbrpy[report]')}[/yellow] to run this command"
            )
            raise typer.Exit(1)

        report_obj: BatteryReport = _get_battery_report()
        history_df = pd.DataFrame([entry.model_dump() for entry in report_obj.History])

        # Generate the capacity history visualization
        fig = px.line(
            history_df,
            x="StartDate",
            y=["DesignCapacity", "FullChargeCapacity"],
            labels={"value": "Capacity (mWh)", "variable": "Type"},
            title="Battery Capacity Over Time",
            template="plotly_dark",
        )  # Save the interactive report to an HTML file
        final_path = output_path.with_suffix(".html")
        fig.write_html(final_path)
        rich.print(f"Report generated successfully at [blue]{final_path}[/blue]")

    elif format in ["default", "raw"]:
        # Determine final path with appropriate extension
        final_path = output_path.with_suffix(f".{format}")

        # Generate the report directly to the specified path
        if format == "default":
            generate_battery_report_html(output_path=final_path)
        else:
            generate_battery_report_xml(output_path=final_path)

        rich.print(f"Report generated successfully at [blue]{final_path}[/blue]")

    else:
        rich.print(
            ":warning:  [bold red]Error:[/bold red] Invalid format. Use 'better', 'default', or 'raw'."
        )
        raise typer.Exit(1)

    # Open HTML reports in browser (for interactive and html formats)
    if format in ["interactive", "html"]:
        webbrowser.open(f"file://{final_path}")


if __name__ == "__main__":
    app()
