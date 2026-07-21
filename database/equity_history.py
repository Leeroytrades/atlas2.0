"""
Atlas AI Trading Assistant 2.0

Equity History Repository
"""

from __future__ import annotations

from datetime import datetime



class EquityHistoryRepository:


    def __init__(self, database):

        self.database = database



    def save(
        self,
        equity: float
    ):

        query = """

        INSERT INTO equity_history

        (
            equity,
            timestamp
        )

        VALUES (?,?)

        """


        self.database.execute(

            query,

            (

                equity,

                datetime.now().isoformat()

            )

        )



    def all(self):

        query = """

        SELECT *

        FROM equity_history

        ORDER BY id ASC

        """


        return self.database.fetch_all(

            query

        )