"""
Atlas AI Trading Assistant 2.0

Dashboard Controller
"""

from __future__ import annotations


from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns


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
    current_equity=10000.00,
):


    console.clear()



    # Scanner

    console.print(

        Panel(

            scanner_table(scans),

            title="Market Scanner"

        )

    )



    # Portfolio

    portfolio_display = portfolio_table(

        portfolio

    )



    # Performance

    performance_display = performance_table(

        metrics

    )



    # Equity

    if equity_history is None:

        equity_history = []



    equity_display = equity_table(

        equity_history,

        current_equity

    )



    console.print(

        Columns(

            [

                Panel(

                    portfolio_display,

                    title="Portfolio"

                ),


                Panel(

                    performance_display,

                    title="Performance Analytics"

                ),

            ]

        )

    )



    console.print(

        Panel(

            equity_display,

            title="Equity Curve"

        )

    )