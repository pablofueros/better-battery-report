"""
Module for defining report formats used across the application.
"""

from enum import Enum


class ReportFormat(str, Enum):
    """Enum for supported report formats across the application."""

    BETTER = "better"  # Custom interactive HTML report
    DEFAULT = "default"  # Windows default HTML report
    RAW = "raw"  # Raw XML data

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
