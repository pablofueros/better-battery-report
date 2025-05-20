"""
Module for defining report formats used across the application.
"""

from enum import Enum


class ReportFormat(str, Enum):
    CUSTOM = "custom"  # Custom interactive HTML report
    STANDARD = "standard"  # Windows standard HTML report
    RAW = "raw"  # Raw XML data used for parsing

    @property
    def is_html(self) -> bool:
        """Return whether this format is HTML-based."""
        return self in [ReportFormat.CUSTOM, ReportFormat.STANDARD]

    @property
    def extension(self) -> str:
        """Return the appropriate file extension for the report format."""
        if self.is_html:
            return ".html"
        else:
            return ".xml"

    @property
    def needs_report_obj(self) -> bool:
        """Return whether this format requires the BatteryReport object."""
        return self == ReportFormat.CUSTOM

    @property
    def browser_viewable(self) -> bool:
        """Return whether this format can be viewed in a browser."""
        return self.is_html
