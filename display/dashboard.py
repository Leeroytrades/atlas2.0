"""
Atlas AI Trading Assistant 2.0

Main Dashboard Display
"""

from rich.console import Console
from rich.panel import Panel
from rich.console import Group

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


    # -------------------------
    # Market Scanner
    # -------------------------

    console.print(
        Panel(
            scanner_table(scans),
            title="Market Scanner"
        )
    )


    # -------------------------
    # Portfolio
    # -------------------------

    console.print(
        Panel(
            portfolio_table(portfolio),
            title="Portfolio"
        )
    )


    # -------------------------
    # Performance
    # -------------------------

    console.print(
        Panel(
            performance_table(metrics),
            title="Performance Analytics"
        )
    )


    # -------------------------
    # Equity Statistics
    # -------------------------

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

    if equity_history:

        clean_history = []

        for row in equity_history:

            try:

                if row[1] is not None:

                    clean_history.append(
                        (
                            row[0],
                            float(row[1])
                        )
                    )

            except Exception:
                continue


        if clean_history:

            chart = build_equity_panel(
                clean_history
            )

            console.print(chart)

        else:

            console.print(
                Panel(
                    "No equity history available",
                    title="Equity Curve"
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

    from rich.table import Table


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


    for index, item in enumerate(history):

        table.add_row(
            str(index + 1),
            f"${item[1]:,.2f}"
        )


    return table