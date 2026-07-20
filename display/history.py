"""
Atlas AI Trading Assistant 2.0

Trade History Display
"""

from rich.table import Table


def history_table(history):

    table = Table(
        title="Trade History"
    )

    table.add_column("Symbol")
    table.add_column("Direction")
    table.add_column("Entry")
    table.add_column("Stop")
    table.add_column("Target")
    table.add_column("R:R")
    table.add_column("Confidence")
    table.add_column("Opened")


    for trade in history:

        table.add_row(

            trade["symbol"],

            trade["direction"],

            f"{trade['entry']:.2f}",

            f"{trade['stop_loss']:.2f}",

            f"{trade['take_profit']:.2f}",

            f"{trade['risk_reward']:.2f}",

            f"{trade['confidence']:.0%}",

            trade["opened"][:19],

        )


    return table