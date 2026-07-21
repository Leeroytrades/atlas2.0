"""
Atlas AI Trading Platform

Dashboard Tables
"""

from __future__ import annotations

from rich.table import Table

from models.scorecard import Scorecard
from models.trade import Trade



def scanner_table(
    results
) -> Table:

    table = Table(
        title="Market Scanner"
    )


    table.add_column(
        "Symbol"
    )

    table.add_column(
        "Score",
        justify="right"
    )

    table.add_column(
        "Bias"
    )

    table.add_column(
        "Confidence",
        justify="right"
    )


    for result in results:

        table.add_row(

            result.symbol,

            str(result.score),

            result.bias,

            f"{result.confidence:.0%}",

        )


    return table



def scorecard_table(
    score: Scorecard
) -> Table:

    table = Table(
        title="Atlas Scorecard"
    )


    table.add_column(
        "Category"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    data = score.summary()


    for key, value in data.items():

        table.add_row(

            str(key),

            str(value)

        )


    return table



def score_table(
    score: Scorecard
) -> Table:

    return scorecard_table(
        score
    )



def trade_table(
    trade: Trade
) -> Table:

    table = Table(
        title="Trade Plan"
    )


    table.add_column(
        "Field"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    rows = [

        ("Symbol", trade.symbol),

        ("Direction", trade.direction),

        ("Entry", f"{trade.entry:.2f}"),

        ("Stop", f"{trade.stop_loss:.2f}"),

        ("Target", f"{trade.take_profit:.2f}"),

        ("Quantity", str(trade.quantity)),

        ("Risk", f"{trade.risk_amount:.2f}"),

        ("Reward", f"{trade.reward_amount:.2f}"),

        ("R:R", f"{trade.risk_reward:.2f}"),

        ("Confidence", f"{trade.confidence:.0%}"),

    ]


    for field, value in rows:

        table.add_row(

            field,

            value

        )


    return table