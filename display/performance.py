"""
Atlas AI Trading Assistant 2.0

Performance Display
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def performance_panel(metrics, statistics=None, equity=None):

    statistics = statistics or {}
    equity = equity or {}

    table = Table(
        show_header=False,
        expand=True,
        pad_edge=False
    )

    table.add_column(style="cyan")
    table.add_column(justify="right")

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
        "Win Rate",
        f'{metrics.get("win_rate",0):.2f}%'
    )

    table.add_row(
        "Profit Factor",
        f'{metrics.get("profit_factor",0):.2f}'
    )

    table.add_row(
        "Net Profit",
        f'${metrics.get("net_profit",0):.2f}'
    )

    table.add_row(
        "Average Win",
        f'${metrics.get("average_win",0):.2f}'
    )

    table.add_row(
        "Average Loss",
        f'${metrics.get("average_loss",0):.2f}'
    )

    table.add_row(
        "Largest Win",
        f'${metrics.get("largest_win",0):.2f}'
    )

    table.add_row(
        "Largest Loss",
        f'${metrics.get("largest_loss",0):.2f}'
    )

    table.add_row(
        "Expectancy",
        f'${metrics.get("expectancy",0):.2f}'
    )

    if equity:

        table.add_section()

        table.add_row(
            "Starting Balance",
            f'${equity.get("starting_balance",0):,.2f}'
        )

        table.add_row(
            "Current Balance",
            f'${equity.get("ending_balance",0):,.2f}'
        )

        table.add_row(
            "Peak Balance",
            f'${equity.get("peak_balance",0):,.2f}'
        )

        table.add_row(
            "Max Drawdown",
            f'${equity.get("max_drawdown",0):,.2f}'
        )

        table.add_row(
            "Return",
            f'${equity.get("total_return",0):,.2f}'
        )

    title = Text(
        "Performance Analytics",
        style="bold green"
    )

    return Panel(

        table,

        title=title,

        border_style="green"

    )