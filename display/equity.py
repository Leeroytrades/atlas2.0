"""
Atlas AI Trading Platform

Equity Display
"""

from __future__ import annotations

from rich.table import Table



def equity_table(
    history,
    current_equity: float,
    starting_balance: float = 10000.00
):


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



    growth = (

        (current_equity - starting_balance)

        /

        starting_balance

        *

        100

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
        "History Points",
        str(len(history))
    )


    return table