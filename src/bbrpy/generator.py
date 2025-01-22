"""Module for generating battery reports using powercfg command. Details:

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
"""

import pathlib
import subprocess
from typing import Optional


def generate_battery_report_xml(
    directory: str = "./reports/",
    filename: str = "battery_report.xml",
    duration: Optional[int] = None,
    delete: bool = False,
) -> str:
    """Generate a battery report using powercfg command."""

    # Create the directory if it does not exist
    filepath = pathlib.Path(directory, filename)
    filepath.parent.mkdir(exist_ok=True, parents=True)

    # Generate the battery report
    cmd = f"powercfg /batteryreport /output {filepath} /xml"
    if duration is not None:
        cmd += f" /duration {duration}"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)

    # Read the report file
    report_xml = filepath.read_text("utf-8")

    # Delete the file if requested
    if delete:
        filepath.unlink()
        filepath.parent.rmdir()

    return report_xml
