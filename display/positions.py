"""
Atlas AI Trading Assistant 2.0

Open Positions Display
"""

from rich.table import Table



def positions_table(
    positions,
    prices=None
):

    table = Table(
        title="Open Positions"
    )


    table.add_column(
        "Symbol"
    )

    table.add_column(
        "Direction"
    )

    table.add_column(
        "Entry",
        justify="right"
    )

    table.add_column(
        "Current",
        justify="right"
    )

    table.add_column(
        "P/L",
        justify="right"
    )

    table.add_column(
        "Status"
    )


    if prices is None:

        prices = {}



    for trade in positions:


        current = prices.get(
            trade.symbol,
            trade.entry
        )


        if trade.direction == "LONG":

            pnl = (
                current - trade.entry
            ) * trade.quantity

        else:

            pnl = (
                trade.entry - current
            ) * trade.quantity



        table.add_row(

            trade.symbol,

            trade.direction,

            f"{trade.entry:.2f}",

            f"{current:.2f}",

            f"{pnl:.2f}",

            trade.status,

        )


    return table