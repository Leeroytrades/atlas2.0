"""
Atlas AI Trading Assistant 2.0

Performance Dashboard Panel
"""

from rich.table import Table



def performance_table(
    metrics
):

    table = Table(
        title="Performance Metrics"
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
        str(
            metrics["total_trades"]
        )
    )


    table.add_row(
        "Closed Trades",
        str(
            metrics["closed_trades"]
        )
    )


    table.add_row(
        "Wins",
        str(
            metrics["wins"]
        )
    )


    table.add_row(
        "Losses",
        str(
            metrics["losses"]
        )
    )


    table.add_row(
        "Win Rate",
        f"{metrics['win_rate']:.2%}"
    )


    table.add_row(
        "Total P/L",
        f"${metrics['total_profit_loss']:.2f}"
    )


    table.add_row(
        "Average Win",
        f"${metrics['average_win']:.2f}"
    )


    table.add_row(
        "Average Loss",
        f"${metrics['average_loss']:.2f}"
    )


    table.add_row(
        "Profit Factor",
        f"{metrics['profit_factor']:.2f}"
    )


    return table