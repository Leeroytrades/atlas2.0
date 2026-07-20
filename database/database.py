"""
Atlas AI Trading Assistant 2.0

SQLite Database Manager
"""

from __future__ import annotations

import sqlite3

from pathlib import Path


class Database:


    def __init__(
        self,
        path: str = "atlas.db"
    ):

        self.path = Path(path)

        self.connection = sqlite3.connect(
            self.path
        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

        self.migrate()



    def execute(
        self,
        query: str,
        parameters: tuple = ()
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        self.connection.commit()

        return cursor



    def fetch_one(
        self,
        query: str,
        parameters: tuple = ()
    ):

        return self.execute(
            query,
            parameters
        ).fetchone()



    def fetch_all(
        self,
        query: str,
        parameters: tuple = ()
    ):

        return self.execute(
            query,
            parameters
        ).fetchall()



    def create_tables(self):

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT NOT NULL,

                direction TEXT NOT NULL,

                entry REAL NOT NULL,

                stop_loss REAL NOT NULL,

                take_profit REAL NOT NULL,

                quantity INTEGER NOT NULL,

                risk_amount REAL NOT NULL,

                reward_amount REAL NOT NULL,

                risk_reward REAL NOT NULL,

                confidence REAL NOT NULL,

                opened TEXT NOT NULL

            )
            """
        )


        self.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                account_balance REAL NOT NULL,

                total_positions INTEGER NOT NULL,

                exposure REAL NOT NULL,

                timestamp TEXT NOT NULL

            )
            """
        )


        self.execute(
            """
            CREATE TABLE IF NOT EXISTS journal (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event TEXT NOT NULL,

                details TEXT,

                timestamp TEXT NOT NULL

            )
            """
        )



    def migrate(self):

        columns = [
            row["name"]
            for row in self.fetch_all(
                "PRAGMA table_info(trades)"
            )
        ]


        migrations = {

            "status":
                "ALTER TABLE trades ADD COLUMN status TEXT DEFAULT 'OPEN'",

            "closed":
                "ALTER TABLE trades ADD COLUMN closed TEXT",

            "exit_price":
                "ALTER TABLE trades ADD COLUMN exit_price REAL",

            "profit_loss":
                "ALTER TABLE trades ADD COLUMN profit_loss REAL",

        }


        for column, sql in migrations.items():

            if column not in columns:

                self.execute(sql)



    def close(self):

        self.connection.close()