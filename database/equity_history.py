"""
Atlas AI Trading Platform 3.0

Equity History Repository

Stores account equity snapshots.

Responsibilities:

- Save equity points
- Retrieve latest equity
- Return equity curve history
"""

from __future__ import annotations

from datetime import datetime



class EquityHistoryRepository:


    def __init__(
        self,
        database,
    ):

        self.database = database



    # ==================================================
    # SAVE EQUITY SNAPSHOT
    # ==================================================

    def save(
        self,
        equity: float,
        trade_id=None,
    ):

        latest = self.latest()


        if latest:

            if round(
                latest["equity"],
                2
            ) == round(
                equity,
                2
            ):

                return latest



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

                round(
                    equity,
                    2
                ),

                datetime.now().isoformat(),

            ),

        )



        return self.latest()



    # ==================================================
    # LATEST EQUITY
    # ==================================================

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



    # ==================================================
    # FULL EQUITY CURVE
    # ==================================================

    def all(self):

        query = """

        SELECT *

        FROM equity_history

        ORDER BY id ASC

        """



        return self.database.fetch_all(

            query

        )



    # ==================================================
    # CLEAR HISTORY
    # ==================================================

    def clear(self):

        self.database.execute(

            """

            DELETE FROM equity_history

            """

        )