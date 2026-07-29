"""
Atlas AI Trading Assistant 2.3

Equity History Repository
"""

from __future__ import annotations

from datetime import datetime



class EquityHistoryRepository:


    def __init__(
        self,
        database
    ):

        self.database = database



    # ---------------------------------------------------------
    # Save Equity Point
    # ---------------------------------------------------------

    def save(
        self,
        equity: float,
        trade_id=None
    ):

        query = """

        INSERT INTO equity_history

        (
            trade_id,
            equity,
            timestamp
        )

        VALUES (?,?,?)

        """


        self.database.execute(

            query,

            (
                trade_id,

                equity,

                datetime.now().isoformat()

            )

        )



    # ---------------------------------------------------------
    # Latest Equity
    # ---------------------------------------------------------

    def latest(self):

        query = """

        SELECT *

        FROM equity_history

        ORDER BY id DESC

        LIMIT 1

        """


        rows = self.database.fetch_all(
            query
        )


        if not rows:

            return None


        return rows[0]



    # ---------------------------------------------------------
    # All History
    # ---------------------------------------------------------

    def all(self):

        query = """

        SELECT *

        FROM equity_history

        ORDER BY id ASC

        """


        return self.database.fetch_all(

            query

        )