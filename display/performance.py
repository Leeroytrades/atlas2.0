"""
Atlas AI Trading Platform

Performance Dashboard Panel
"""

from __future__ import annotations

from rich.panel import Panel
from rich.table import Table



def performance_table(
    metrics: dict
):

    table = Table(
        title="Atlas Performance"
    )


    table.add_column(
        "Metric"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    table.add_row(
        "Total Trades",
        str(metrics.get("total_trades", 0))
    )


    table.add_row(
        "Open Trades",
        str(metrics.get("open_trades", 0))
    )


    table.add_row(
        "Closed Trades",
        str(metrics.get("closed_trades", 0))
    )


    table.add_row(
        "Wins",
        str(metrics.get("wins", 0))
    )


    table.add_row(
        "Losses",
        str(metrics.get("losses", 0))
    )


    table.add_row(
        "Win Rate",
        f"{metrics.get('win_rate',0)}%"
    )


    table.add_row(
        "Net Profit",
        f"${metrics.get('net_profit',0):,.2f}"
    )


    table.add_row(
        "Equity",
        f"${metrics.get('equity',0):,.2f}"
    )


    table.add_row(
        "Growth",
        f"{metrics.get('growth_percent',0)}%"
    )


    table.add_row(
        "Profit Factor",
        str(metrics.get("profit_factor",0))
    )


    table.add_row(
        "Expectancy",
        f"${metrics.get('expectancy',0):,.2f}"
    )


    drawdown = metrics.get(
        "drawdown",
        {}
    )


    table.add_row(
        "Max Drawdown",
        f"{drawdown.get('maximum_drawdown',0)}%"
    )


    return table



def performance_panel(
    metrics: dict
):

    return Panel(

        performance_table(
            metrics
        ),

        title="Performance Analytics",

        border_style="magenta",

    )