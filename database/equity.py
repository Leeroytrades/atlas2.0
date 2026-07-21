"""
Atlas AI Trading Platform

Equity Repository

Handles:
- Saving equity history
- Loading equity history
- Latest equity value
"""

from __future__ import annotations

from datetime import datetime



class EquityRepository:


    def __init__(
        self,
        database
    ):

        self.database = database



    def save(
        self,
        equity: float,
        trade_id: int | None = None
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


        return self.database.execute(

            query,

            (

                trade_id,

                equity,

                datetime.now().isoformat(),

            )

        )



    def history(self):


        query = """

        SELECT *

        FROM equity_history

        ORDER BY id ASC

        """


        return self.database.fetch_all(

            query

        )



    def latest(self):


        query = """

        SELECT *

        FROM equity_history

        ORDER BY id DESC

        LIMIT 1

        """


        return self.database.fetch_one(

            query

        )



    def values(self):


        rows = self.history()


        return [

            row["equity"]

            for row in rows

        ]