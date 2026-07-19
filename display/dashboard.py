"""
Atlas Dashboard
"""

from rich.console import Console

from display.theme import ATLAS_THEME
from display.panels import title_panel
from display.tables import score_table
from display.tables import trade_table
from display.scanner_table import scanner_table

console = Console(theme=ATLAS_THEME)


def show_dashboard(results, score, trade):

    console.clear()

    console.print(title_panel())

    console.print()

    console.print(scanner_table(results))

    console.print()

    console.print(score_table(score))

    console.print()

    console.print(trade_table(trade))

    console.print()

    console.print("[bold green]Analysis Complete[/bold green]")