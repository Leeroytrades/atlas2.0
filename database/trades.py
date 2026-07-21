"""
Atlas AI Trading Platform

Trade Repository

Handles all database interaction for trades.
"""

from __future__ import annotations

from datetime import datetime

from models.trade import Trade


class TradeRepository:
    """
    SQLite repository for Trade objects.
    """

    def __init__(
        self,
        database,
    ):

        self.database = database

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def save(
        self,
        trade: Trade,
    ) -> Trade:

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
                trade.status,

            ),

        )

        trade.id = cursor.lastrowid

        return trade

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(
        self,
        trade: Trade,
    ) -> Trade:

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

                trade.exit_price,

                trade.profit_loss,

                trade.id,

            ),

        )

        return trade

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close_trade(
        self,
        trade: Trade,
        exit_price: float,
    ) -> Trade:

        trade.close(
            exit_price
        )

        self.update(
            trade
        )

        return trade

    # ---------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------

    def open_trades(
        self,
    ) -> list[Trade]:

        rows = self.database.fetch_all(

            """
            SELECT *

            FROM trades

            WHERE status='OPEN'

            ORDER BY opened ASC
            """

        )

        return [

            self._row_to_trade(row)

            for row in rows

        ]

    def closed_trades(
        self,
    ) -> list[Trade]:

        rows = self.database.fetch_all(

            """
            SELECT *

            FROM trades

            WHERE status='CLOSED'

            ORDER BY closed ASC
            """

        )

        return [

            self._row_to_trade(row)

            for row in rows

        ]

    def recent(
        self,
        limit: int = 20,
    ):

        return self.database.fetch_all(

            """
            SELECT *

            FROM trades

            ORDER BY id DESC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    # ---------------------------------------------------------
    # INTERNAL
    # ---------------------------------------------------------

    def _row_to_trade(
        self,
        row,
    ) -> Trade:

        trade = Trade(

            id=row["id"],

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

            status=row["status"],

            opened=datetime.fromisoformat(
                row["opened"]
            ),

            closed=(

                datetime.fromisoformat(
                    row["closed"]
                )

                if row["closed"]

                else None

            ),

            exit_price=row["exit_price"],

            profit_loss=row["profit_loss"] or 0.0,

        )

        return trade