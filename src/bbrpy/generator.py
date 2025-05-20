"""
Module for generating battery reports using powercfg command. Details:

POWERCFG /BATTERYREPORT [/OUTPUT <FILENAME>] [/XML] [/TRANSFORMXML <FILENAME.XML>]


Description:
    Generates a report of battery usage characteristics over the life of the system.
    system. The BATTERYREPORT command will generate an HTML report file at the current path.
    current path.

List of parameters:
    /OUTPUT <FILE NAME>     Specify the path and filename to store the battery report file.
    /XML                   Formats the report file in XML format.
    /DURATION <DAYS>       Specify the number of days to be analysed for the report.
    /TRANSFORMXML <FILENAME.XML>   Reformat an XML report file as HTML.

Examples:
    POWERCFG /BATTERYREPORT
    POWERCFG /BATTERYREPORT /OUTPUT "batteryreport.html"
    POWERCFG /BATTERYREPORT /OUTPUT "batteryreport.xml" /XML
    POWERCFG /BATTERYREPORT /TRANSFORMXML "batteryreport.xml"
    POWERCFG /BATTERYREPORT /TRANSFORMXML "batteryreport.xml" /OUTPUT "batteryreport.html"

Note:
    The /XML command line switch is not supported with /TRANSFORMXML.
    The /DURATION command line switch is not supported with /TRANSFORMXML.
"""

import pathlib
import platform
import subprocess
import tempfile
from typing import Literal

from .exceptions import PlatformError
from .utils import is_platform_windows


def _generate_battery_report(
    format: Literal["html", "xml"] = "html",
    output_path: pathlib.Path | None = None,
) -> str:
    """
    Generate a battery report using the powercfg command.

    Args:
        format: The format of the report, either "html" or "xml".
            (default: "html").
        output_path (pathlib.Path, optional): The path where the report should be saved.
            If None, a temporary directory will be used (default: None).
    Returns:
        str: The content of the generated battery report file.
    Raises:
        PlatformError: If the tool is run on a non-Windows platform.
    """
    # Check if running on Windows
    if not is_platform_windows():
        raise PlatformError(
            "This tool is designed for Windows systems only as it relies on the 'powercfg' command.\n"
            f"For the time being, it cannot run on your current platform: {platform.system()}"
        )

    # Handle temporary directories or use provided path
    if output_path is None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create filepath in temporary directory
            filepath = pathlib.Path(temp_dir) / f"report.{format}"
            return _run_battery_report(filepath, format)
    else:
        # Use provided output path with appropriate extension
        filepath = output_path.with_suffix(f".{format}")
        return _run_battery_report(filepath, format)


def _run_battery_report(filepath: pathlib.Path, format: Literal["html", "xml"]) -> str:
    """
    Execute the powercfg command to generate a battery report and read its contents.

    Args:
        filepath: The full path where the report file will be saved
        format: The format of the report ("html" or "xml")

    Returns:
        The content of the generated report file
    """
    # Build command with appropriate flags
    cmd = ["powercfg", "/batteryreport", "/output", str(filepath)]
    if format == "xml":
        cmd.append("/xml")

    # Run command and read back the file
    subprocess.run(cmd, stdout=subprocess.DEVNULL, check=True)
    return filepath.read_text("utf-8")


def generate_battery_report_xml(output_path: pathlib.Path | None = None) -> str:
    """
    Returns the content of the battery report XML file.

    Args:
        output_path (pathlib.Path, optional): The path where the report should be saved.
            If None, a temporary directory will be used (default: None).

    Returns:
        str: The content of the generated battery report XML file.
    Raises:
        PlatformError: If the tool is run on a non-Windows platform.
    """
    return _generate_battery_report(
        format="xml",
        output_path=output_path,
    )


def generate_battery_report_html(output_path: pathlib.Path | None = None) -> str:
    """
    Returns the content of the battery report HTML file.

    Args:
        output_path (pathlib.Path, optional): The path where the report should be saved.
            If None, a temporary directory will be used (default: None).

    Returns:
        str: The content of the generated battery report HTML file.
    Raises:
        PlatformError: If the tool is run on a non-Windows platform.
    """
    return _generate_battery_report(
        format="html",
        output_path=output_path,
    )
