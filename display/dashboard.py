"""
Atlas AI Trading Assistant 2.0

Dashboard
"""

from rich.console import Console

from display.theme import ATLAS_THEME

from display.panels import title_panel

from display.tables import score_table

from display.tables import trade_table

from display.scanner_table import scanner_table

from display.positions import positions_table

from display.performance import performance_table



console = Console(
    theme=ATLAS_THEME
)



def show_dashboard(
    results,
    score,
    trade,
    positions=None,
    prices=None,
    metrics=None
):

    console.clear()


    console.print(
        title_panel()
    )


    console.print()


    console.print(
        scanner_table(results)
    )


    console.print()


    console.print(
        score_table(score)
    )


    console.print()


    console.print(
        trade_table(trade)
    )


    console.print()



    if positions:

        console.print(
            positions_table(
                positions,
                prices
            )
        )

        console.print()



    if metrics:

        console.print(
            performance_table(
                metrics
            )
        )

        console.print()



    console.print(
        "[bold green]Analysis Complete[/bold green]"
    )