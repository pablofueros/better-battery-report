import webbrowser
from pathlib import Path
from typing import Protocol

import rich
import typer
from rich.markup import escape

from .exceptions import PlatformError
from .formats import ReportFormat
from .generator import generate_battery_report_html, generate_battery_report_xml
from .models import BatteryReport
from .version import __version__

app = typer.Typer()


def _display_version(value: bool) -> None:
    """Display the version of the application and exit."""
    if value:
        typer.echo(f"bbrpy {__version__}")
        raise typer.Exit()


def _get_battery_report() -> BatteryReport:
    """Generates the battery report and handles PlatformError."""
    try:
        return BatteryReport.generate()
    except PlatformError as e:
        rich.print(f":warning:  [bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


def _validate_report_format(format: str) -> ReportFormat:
    """Validate the report format and return it if valid."""
    try:
        return ReportFormat(format.lower())
    except ValueError:
        valid_formats = [f.value for f in ReportFormat]
        rich.print(
            f":warning:  [bold red]Error:[/bold red] Invalid format '{format}'. "
            f"Use {', '.join([f'[yellow]{f}[/yellow]' for f in valid_formats])}"
        )
        raise typer.Exit(code=1)


def _generate_custom_report(
    output_path: Path,
    report_obj: BatteryReport,
) -> Path:
    """Generate the 'custom' interactive HTML report with Plotly."""
    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        rich.print(
            ":warning:  [bold red]Error: [/bold red] Missing extra dependencies!\n"
            f"Use [yellow]{escape('bbrpy[report]')}[/yellow] to run this command"
        )
        raise typer.Exit(1)

    # Prepare the data frame from the report history
    history_df = pd.DataFrame([entry.model_dump() for entry in report_obj.History])

    # Generate the capacity history visualization
    fig = px.line(
        history_df,
        x="StartDate",
        y=["DesignCapacity", "FullChargeCapacity"],
        labels={"value": "Capacity (mWh)", "variable": "Type"},
        title="Battery Capacity Over Time",
        template="plotly_dark",
    )

    # Save the interactive report to an HTML file
    final_path = output_path.with_suffix(ReportFormat.CUSTOM.extension)
    fig.write_html(final_path)
    return final_path


def _generate_standard_report(output_path: Path) -> Path:
    """Generate the standard Windows HTML battery report."""
    final_path = output_path.with_suffix(ReportFormat.STANDARD.extension)
    generate_battery_report_html(output_path=final_path)
    return final_path


def _generate_raw_report(output_path: Path) -> Path:
    """Generate the raw XML battery report data."""
    final_path = output_path.with_suffix(ReportFormat.RAW.extension)
    generate_battery_report_xml(output_path=final_path)
    return final_path


# Protocol for report handlers (both with and without BatteryReport)
class ReportHandlerProtocol(Protocol):
    """Protocol for report generation functions."""

    def __call__(self, output_path: Path, *args, **kwargs) -> Path: ...


# Registry mapping format enum values to their generator functions
FORMAT_HANDLERS: dict[ReportFormat, ReportHandlerProtocol] = {
    ReportFormat.CUSTOM: _generate_custom_report,
    ReportFormat.STANDARD: _generate_standard_report,
    ReportFormat.RAW: _generate_raw_report,
}


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
        "custom",
        "--format",
        "-f",
        help="Report format: 'custom' (interactive html), 'standard' (Windows html), or 'raw' (xml data)",
    ),
):
    """Generate a battery report in various formats."""

    # Validate the report format
    format_enum = _validate_report_format(format)

    # Create the output directory if it doesn't exist
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get the appropriate handler from our registry
    handler = FORMAT_HANDLERS[format_enum]

    # Generate the report
    if format_enum.needs_report_obj:
        # Only fetch the report object when needed
        report_obj = _get_battery_report()
        final_path = handler(output_path, report_obj)
    else:
        final_path = handler(output_path)

    # Print success message
    rich.print(f"Report generated successfully at [blue]{final_path}[/blue]")

    # Open HTML reports in browser if applicable
    if format_enum.browser_viewable:
        webbrowser.open(f"file://{final_path}")


if __name__ == "__main__":
    app()
