"""
Atlas Console Theme
"""

from rich.theme import Theme

ATLAS_THEME = Theme(
    {
        "title": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "danger": "bold red",
        "info": "bright_white",
        "number": "bold magenta",
    }
)