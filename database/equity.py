"""
Atlas AI Trading Assistant 2.2

Equity History Repository

Stores account equity snapshots.
"""

from __future__ import annotations

from datetime import datetime


class EquityHistoryRepository:


    def __init__(
        self,
        database
    ):

        self.database = database



    def save(
        self,
        equity: float,
        trade_id=None
    ):

        """
        Save equity snapshot only
        when equity changes.
        """

        latest = self.database.fetch_all(

            """
            SELECT equity
            FROM equity_history
            ORDER BY id DESC
            LIMIT 1
            """

        )


        if latest:

            last_equity = float(
                latest[0]["equity"]
            )

            if last_equity == equity:
                return



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



    def all(self):

        return self.database.fetch_all(

            """

            SELECT *

            FROM equity_history

            ORDER BY id ASC

            """

        )



    def latest(self):

        rows = self.database.fetch_all(

            """

            SELECT *

            FROM equity_history

            ORDER BY id DESC

            LIMIT 1

            """

        )

        if rows:
            return rows[0]

        return None