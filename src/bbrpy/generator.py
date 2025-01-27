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

Note:
    The /XML command line switch is not supported with /TRANSFORMXML.
    The /DURATION command line switch is not supported with /TRANSFORMXML.

Returns the content of the battery report XML file.
The file is created in a temporary directory and deleted after reading.
"""

import pathlib
import subprocess
import tempfile


def generate_battery_report_xml() -> str:
    """Returns the content of the battery report XML file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the file path for the report file
        filepath = pathlib.Path(temp_dir, "report.xml")
        # Generate the battery report in XML format
        cmd = f"powercfg /batteryreport /output {filepath} /xml"
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        # Read and return the report content
        return filepath.read_text("utf-8")
