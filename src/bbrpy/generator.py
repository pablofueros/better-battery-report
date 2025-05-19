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
from enum import Enum

from .exceptions import PlatformError
from .utils import is_platform_windows


class ReportFormat(Enum):
    HTML = "html"
    XML = "xml"


def _generate_battery_report(format: ReportFormat = ReportFormat.HTML) -> str:
    """
    Generate a battery report using the powercfg command.

    Args:
        format (ReportFormat): The format of the report, either ReportFormat.HTML or ReportFormat.XML.
            (default: ReportFormat.HTML).
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

    with tempfile.TemporaryDirectory() as temp_dir:
        base = pathlib.Path(temp_dir) / "report"
        is_xml = format == ReportFormat.XML
        filepath = base.with_suffix(f".{format.value}")
        cmd = ["powercfg", "/batteryreport", "/output", str(filepath)]
        if is_xml:
            cmd.append("/xml")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, check=True)
        return filepath.read_text("utf-8")


def generate_battery_report_xml() -> str:
    """
    Returns the content of the battery report XML file.

    Returns:
        str: The content of the generated battery report XML file.
    Raises:
        PlatformError: If the tool is run on a non-Windows platform.
    """
    return _generate_battery_report(format=ReportFormat.XML)


def generate_battery_report_html() -> str:
    """
    Returns the content of the battery report HTML file.

    Returns:
        str: The content of the generated battery report HTML file.
    Raises:
        PlatformError: If the tool is run on a non-Windows platform.
    """
    return _generate_battery_report(format=ReportFormat.HTML)
