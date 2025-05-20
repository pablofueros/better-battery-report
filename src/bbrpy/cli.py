import pathlib
import webbrowser
from enum import Enum
from typing import Protocol

import rich
import typer
from rich.markup import escape

from .exceptions import PlatformError
from .generator import generate_battery_report_html, generate_battery_report_xml
from .models import BatteryReport
from .version import __version__

app = typer.Typer()


class ReportFormat(str, Enum):
    BETTER = "better"
    DEFAULT = "default"
    RAW = "raw"

    @property
    def extension(self) -> str:
        """Return the appropriate file extension for the report format."""
        if self in [ReportFormat.BETTER, ReportFormat.DEFAULT]:
            return ".html"
        elif self == ReportFormat.RAW:
            return ".xml"
        return ""

    @property
    def needs_report_obj(self) -> bool:
        """Return whether this format requires the BatteryReport object."""
        return self == ReportFormat.BETTER

    @property
    def browser_viewable(self) -> bool:
        """Return whether this format can be viewed in a browser."""
        return self in [ReportFormat.BETTER, ReportFormat.DEFAULT]


# Protocol for report handlers (both with and without BatteryReport)
class ReportHandlerProtocol(Protocol):
    """Protocol for report generation functions."""

    def __call__(self, output_path: pathlib.Path, *args, **kwargs) -> pathlib.Path: ...


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


def _validate_report_format(format_str: str) -> ReportFormat:
    """Validate the report format and return it if valid."""
    try:
        return ReportFormat(format_str.lower())
    except ValueError:
        valid_formats = [f.value for f in ReportFormat]
        rich.print(
            f":warning:  [bold red]Error:[/bold red] Invalid format '{format_str}'. "
            f"Use {', '.join([f'[yellow]{f}[/yellow]' for f in valid_formats])}"
        )
        raise typer.Exit(1)


def _generate_better_report(
    output_path: pathlib.Path, report_obj: BatteryReport
) -> pathlib.Path:
    """Generate the 'better' interactive HTML report with Plotly."""
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
    final_path = output_path.with_suffix(ReportFormat.BETTER.extension)
    fig.write_html(final_path)
    return final_path


def _generate_default_report(output_path: pathlib.Path) -> pathlib.Path:
    """Generate the default Windows HTML battery report."""
    final_path = output_path.with_suffix(ReportFormat.DEFAULT.extension)
    generate_battery_report_html(output_path=final_path)
    return final_path


def _generate_raw_report(output_path: pathlib.Path) -> pathlib.Path:
    """Generate the raw XML battery report data."""
    final_path = output_path.with_suffix(ReportFormat.RAW.extension)
    generate_battery_report_xml(output_path=final_path)
    return final_path


# Registry mapping format enum values to their generator functions
FORMAT_HANDLERS: dict[ReportFormat, ReportHandlerProtocol] = {
    ReportFormat.BETTER: _generate_better_report,
    ReportFormat.DEFAULT: _generate_default_report,
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
        "better",
        "--format",
        "-f",
        help="Report format: 'better' (custom html), 'default' (Windows html), or 'raw' (xml data)",
    ),
):
    """Generate a battery report in various formats."""

    # Validate the report format
    format_enum = _validate_report_format(format)

    # Create the output directory if it doesn't exist
    output_path = pathlib.Path(output).resolve()
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
