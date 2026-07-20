"""
Atlas AI Trading Assistant 2.0

Portfolio Repository
"""

from __future__ import annotations

from datetime import datetime

from database.database import Database



class PortfolioRepository:


    def __init__(
        self,
        database: Database
    ):

        self.database = database



    def save(
        self,
        portfolio
    ):

        result = self.database.execute(
            """
            INSERT INTO portfolio (

                account_balance,

                total_positions,

                exposure,

                timestamp

            )

            VALUES (?, ?, ?, ?)

            """,
            (

                portfolio.account_balance,

                portfolio.total_positions,

                portfolio.exposure,

                datetime.now().isoformat(),

            )
        )

        return result.lastrowid



    def latest(self):

        row = self.database.fetch_one(
            """
            SELECT *

            FROM portfolio

            ORDER BY id DESC

            LIMIT 1

            """
        )


        if row:

            return dict(row)


        return None



    def history(self):

        rows = self.database.fetch_all(
            """
            SELECT *

            FROM portfolio

            ORDER BY id DESC

            """
        )


        return [

            dict(row)

            for row in rows

        ]