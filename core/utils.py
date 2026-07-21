"""
Atlas utility functions.
"""

from __future__ import annotations


def percentage(value: float, percent: float) -> float:
    """Return percentage of a value."""
    return value * (percent / 100)


def safe_round(value: float | None, digits: int = 2) -> float:
    """Safely round numbers."""
    if value is None:
        return 0.0

    return round(value, digits)