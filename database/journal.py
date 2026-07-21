"""
Atlas AI Trading Assistant

Trade Journal Repository
"""

from __future__ import annotations

from datetime import datetime


class JournalRepository:

    def __init__(self, database):
        self.db = database


    def record_signal(
        self,
        symbol: str,
        direction: str,
        entry: float,
        score: int,
        confidence: float,
        trend: int,
        momentum: int,
        volatility: int,
        volume: int,
        market_condition: str = "UNKNOWN"
    ):

        self.db.execute(
            """
            INSERT INTO journal (

                symbol,
                direction,
                entry_price,
                score,
                confidence,
                trend,
                momentum,
                volatility,
                volume,
                market_condition,
                created

            )

            VALUES (?,?,?,?,?,?,?,?,?,?,?)

            """,
            (
                symbol,
                direction,
                entry,
                score,
                confidence,
                trend,
                momentum,
                volatility,
                volume,
                market_condition,
                datetime.now().isoformat()
            )
        )


    def close_trade(
        self,
        journal_id: int,
        exit_price: float,
        profit_loss: float,
        outcome: str
    ):

        self.db.execute(
            """
            UPDATE journal

            SET

                exit_price=?,
                profit_loss=?,
                outcome=?

            WHERE id=?

            """,
            (
                exit_price,
                profit_loss,
                outcome,
                journal_id
            )
        )


    def history(self):

        return self.db.fetch_all(
            """
            SELECT *

            FROM journal

            ORDER BY id DESC

            """
        )


    def total_trades(self):

        result = self.db.fetch_one(
            """
            SELECT COUNT(*) as total

            FROM journal

            """
        )

        return result["total"]


    def winners(self):

        result = self.db.fetch_one(
            """
            SELECT COUNT(*) as wins

            FROM journal

            WHERE outcome='WIN'

            """
        )

        return result["wins"]


    def win_rate(self):

        total = self.total_trades()

        if total == 0:
            return 0

        return round(
            (self.winners() / total) * 100,
            2
        )