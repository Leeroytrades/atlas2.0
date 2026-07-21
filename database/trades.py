"""
Atlas AI Trading Assistant 2.0

Trade Repository

Handles:
- Saving trades
- Loading trades
- Updating trades
- Closing trades
- Trade history
"""

from __future__ import annotations

from datetime import datetime

from atlas.trade import Trade


class TradeRepository:

    def __init__(self, database):

        self.database = database

    def save(self, trade: Trade):

        query = """
        INSERT INTO trades (

            symbol,
            direction,
            entry,
            stop_loss,
            take_profit,
            quantity,
            risk_amount,
            reward_amount,
            risk_reward,
            confidence,
            opened,
            status

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """

        cursor = self.database.execute(

            query,

            (

                trade.symbol,
                trade.direction,
                trade.entry,
                trade.stop_loss,
                trade.take_profit,
                trade.quantity,
                trade.risk_amount,
                trade.reward_amount,
                trade.risk_reward,
                trade.confidence,
                trade.opened.isoformat(),
                "OPEN",

            )

        )

        trade.id = cursor.lastrowid

        return trade

    def update(self, trade):

        query = """
        UPDATE trades

        SET

            status=?,
            closed=?,
            exit_price=?,
            profit_loss=?

        WHERE id=?
        """

        self.database.execute(

            query,

            (

                trade.status,

                trade.closed.isoformat()
                if trade.closed
                else None,

                getattr(
                    trade,
                    "exit_price",
                    None
                ),

                getattr(
                    trade,
                    "profit_loss",
                    None
                ),

                trade.id,

            )

        )

        return trade

    def close_trade(self, trade, exit_price: float):

        if trade.direction == "LONG":

            profit_loss = (

                exit_price - trade.entry

            ) * trade.quantity

        else:

            profit_loss = (

                trade.entry - exit_price

            ) * trade.quantity

        trade.status = "CLOSED"

        trade.closed = datetime.now()

        trade.exit_price = exit_price

        trade.profit_loss = round(
            profit_loss,
            2
        )

        self.update(trade)

        return trade

    def open_trades(self):

        query = """
        SELECT *

        FROM trades

        WHERE status='OPEN'

        ORDER BY opened ASC
        """

        rows = self.database.fetch_all(query)

        return [

            self._row_to_trade(row)

            for row in rows

        ]

    def get_closed_trades(self):

        query = """
        SELECT *

        FROM trades

        WHERE status='CLOSED'

        ORDER BY closed ASC
        """

        rows = self.database.fetch_all(query)

        return [

            self._row_to_trade(row)

            for row in rows

        ]

    def recent(self, limit=20):

        query = """
        SELECT *

        FROM trades

        ORDER BY id DESC

        LIMIT ?
        """

        return self.database.fetch_all(

            query,

            (

                limit,

            )

        )

    def _row_to_trade(self, row):

        trade = Trade(

            symbol=row["symbol"],

            direction=row["direction"],

            entry=row["entry"],

            stop_loss=row["stop_loss"],

            take_profit=row["take_profit"],

            quantity=row["quantity"],

            risk_amount=row["risk_amount"],

            reward_amount=row["reward_amount"],

            risk_reward=row["risk_reward"],

            confidence=row["confidence"],

        )

        trade.id = row["id"]

        trade.status = row["status"]

        trade.opened = datetime.fromisoformat(
            row["opened"]
        )

        trade.closed = (

            datetime.fromisoformat(
                row["closed"]
            )

            if row["closed"]

            else None

        )

        trade.exit_price = row["exit_price"]

        trade.profit_loss = row["profit_loss"]

        return trade