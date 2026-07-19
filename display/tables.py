"""
Atlas Tables
"""

from rich.table import Table

from models.scorecard import Scorecard
from risk.trade import Trade


def score_table(score: Scorecard) -> Table:

    table = Table(title="Atlas Scorecard")

    table.add_column("Category")
    table.add_column("Value", justify="right")

    data = score.summary()

    for k, v in data.items():
        table.add_row(str(k), str(v))

    return table


def trade_table(trade: Trade) -> Table:

    table = Table(title="Trade Plan")

    table.add_column("Field")
    table.add_column("Value", justify="right")

    table.add_row("Symbol", trade.symbol)
    table.add_row("Direction", trade.direction)
    table.add_row("Entry", f"{trade.entry:.2f}")
    table.add_row("Stop", f"{trade.stop_loss:.2f}")
    table.add_row("Target", f"{trade.take_profit:.2f}")
    table.add_row("Quantity", str(trade.quantity))
    table.add_row("Risk", f"{trade.risk_amount:.2f}")
    table.add_row("Reward", f"{trade.reward_amount:.2f}")
    table.add_row("R:R", f"{trade.risk_reward:.2f}")
    table.add_row("Confidence", f"{trade.confidence:.0%}")

    return table