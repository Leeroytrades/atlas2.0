"""
Atlas AI Trading Platform

Equity Dashboard Display
"""

from rich.table import Table

from performance.equity_chart import (
    build_equity_curve,
    calculate_growth,
)


def equity_table(
    history,
    current_equity: float = 0.0
) -> Table:
    """
    Display equity statistics.
    """

    table = Table(
        title="Equity Curve"
    )

    table.add_column(
        "Metric"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    starting_balance = 10000.00


    try:

        curve = build_equity_curve(
            history
        )

    except Exception:

        curve = []


    try:

        growth = calculate_growth(
            current_equity
        )

    except Exception:

        growth = (
            ((current_equity - starting_balance)
             / starting_balance)
            * 100
        )


    table.add_row(
        "Starting Balance",
        f"${starting_balance:,.2f}"
    )

    table.add_row(
        "Current Equity",
        f"${current_equity:,.2f}"
    )

    table.add_row(
        "Growth",
        f"{growth:.2f}%"
    )

    table.add_row(
        "Equity Points",
        str(len(curve))
    )


    return table