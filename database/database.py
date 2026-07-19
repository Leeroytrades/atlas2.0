"""
Atlas AI Trading Assistant

SQLite Database
"""

from pathlib import Path
import sqlite3


DATABASE_FILE = Path("atlas.db")


class AtlasDatabase:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_FILE)

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                direction TEXT,

                confidence REAL,

                entry REAL,

                stop REAL,

                target REAL,

                risk_reward REAL,

                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        self.connection.commit()

    def save_trade(self, trade):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO trades
            (
                symbol,
                direction,
                confidence,
                entry,
                stop,
                target,
                risk_reward
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trade.symbol,
                trade.direction,
                trade.confidence,
                trade.entry,
                trade.stop,
                trade.target,
                trade.risk_reward,
            ),
        )

        self.connection.commit()

    def all_trades(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM trades
            ORDER BY created DESC
            """
        )

        return cursor.fetchall()