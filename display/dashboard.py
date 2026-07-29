"""
Atlas AI Trading Assistant 2.0

Main Dashboard Display
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from display.scanner_table import scanner_table
from display.portfolio import portfolio_table
from display.performance import performance_table
from display.equity import equity_table


console = Console()



def show_dashboard(
    scans,
    portfolio,
    metrics,
    equity_history=None,
    current_equity=0.0
):
    """
    Render Atlas dashboard.
    """


    console.print(
        Panel(
            scanner_table(scans),
            title="Market Scanner"
        )
    )


    console.print(
        Panel(
            portfolio_table(portfolio),
            title="Portfolio"
        )
    )


    console.print(
        Panel(
            performance_table(metrics),
            title="Performance Analytics"
        )
    )


    console.print(
        Panel(
            equity_table(
                equity_history,
                current_equity
            ),
            title="Equity Statistics"
        )
    )


    # -------------------------
    # Equity Curve
    # -------------------------

    clean_history = []


    if equity_history:

        for row in equity_history:

            try:

                clean_history.append(

                    float(
                        row["equity"]
                    )

                )

            except Exception:

                continue



    if clean_history:

        console.print(

            build_equity_panel(
                clean_history
            )

        )

    else:

        console.print(

            Panel(
                "No equity history available",
                title="Equity Curve"
            )

        )



def build_equity_panel(history):

    """
    Simple equity history display.
    """

    table = Table(
        title="Equity Curve"
    )


    table.add_column(
        "Point"
    )


    table.add_column(
        "Equity",
        justify="right"
    )


    for index, equity in enumerate(history):

        table.add_row(

            str(index + 1),

            f"${equity:,.2f}"

        )


    return table