"""
Utility functions for the bbrpy package.
"""

import platform


def is_platform_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"
