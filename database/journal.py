"""
Atlas AI Trading Assistant 2.0

Trading Journal Repository
"""

from __future__ import annotations

from datetime import datetime

from database.database import Database


class JournalRepository:

    def __init__(self, database: Database):

        self.database = database


    def log(
        self,
        event: str,
        details: str = ""
    ):

        result = self.database.execute(
            """
            INSERT INTO journal (

                event,
                details,
                timestamp

            )

            VALUES (?, ?, ?)

            """,
            (
                event,
                details,
                datetime.now().isoformat(),
            )
        )

        return result.lastrowid


    def history(self):

        rows = self.database.fetch_all(
            """
            SELECT *

            FROM journal

            ORDER BY id DESC

            """
        )

        return [
            dict(row)
            for row in rows
        ]