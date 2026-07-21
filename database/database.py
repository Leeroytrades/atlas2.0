"""
Atlas AI Trading Platform

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

                symbol TEXT,
                direction TEXT,

                entry_price REAL,
                exit_price REAL,

                score INTEGER,
                confidence REAL,

                trend TEXT,
                momentum TEXT,
                volatility TEXT,
                volume TEXT,

                market_condition TEXT,

                outcome TEXT DEFAULT 'OPEN',

                profit_loss REAL DEFAULT 0,

                notes TEXT,

                created TEXT

            )
            """
        )


        self.execute(
            """
            CREATE TABLE IF NOT EXISTS equity_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                trade_id INTEGER,

                equity REAL NOT NULL,

                timestamp TEXT NOT NULL

            )
            """
        )


    def migrate(self):

        migrations = {

            "trades": {

                "status":
                "ALTER TABLE trades ADD COLUMN status TEXT DEFAULT 'OPEN'",

                "closed":
                "ALTER TABLE trades ADD COLUMN closed TEXT",

                "exit_price":
                "ALTER TABLE trades ADD COLUMN exit_price REAL",

                "profit_loss":
                "ALTER TABLE trades ADD COLUMN profit_loss REAL",
            },


            "journal": {

                "symbol":
                "ALTER TABLE journal ADD COLUMN symbol TEXT",

                "direction":
                "ALTER TABLE journal ADD COLUMN direction TEXT",

                "entry_price":
                "ALTER TABLE journal ADD COLUMN entry_price REAL",

                "exit_price":
                "ALTER TABLE journal ADD COLUMN exit_price REAL",

                "score":
                "ALTER TABLE journal ADD COLUMN score INTEGER",

                "confidence":
                "ALTER TABLE journal ADD COLUMN confidence REAL",

                "trend":
                "ALTER TABLE journal ADD COLUMN trend TEXT",

                "momentum":
                "ALTER TABLE journal ADD COLUMN momentum TEXT",

                "volatility":
                "ALTER TABLE journal ADD COLUMN volatility TEXT",

                "volume":
                "ALTER TABLE journal ADD COLUMN volume TEXT",

                "market_condition":
                "ALTER TABLE journal ADD COLUMN market_condition TEXT",

                "outcome":
                "ALTER TABLE journal ADD COLUMN outcome TEXT DEFAULT 'OPEN'",

                "profit_loss":
                "ALTER TABLE journal ADD COLUMN profit_loss REAL DEFAULT 0",

                "notes":
                "ALTER TABLE journal ADD COLUMN notes TEXT",

                "created":
                "ALTER TABLE journal ADD COLUMN created TEXT",
            }

        }


        for table, columns in migrations.items():

            existing = [
                row["name"]
                for row in self.fetch_all(
                    f"PRAGMA table_info({table})"
                )
            ]


            for column, sql in columns.items():

                if column not in existing:

                    self.execute(sql)


    def close(self):

        self.connection.close()