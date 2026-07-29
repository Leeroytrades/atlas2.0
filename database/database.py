"""
Atlas AI Trading Platform

SQLite Database Manager
Atlas 2.2
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """
    Atlas database manager.
    """

    def __init__(
        self,
        path: str = "atlas.db",
    ):

        self.path = Path(path)

        self.connection = sqlite3.connect(self.path)

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    def execute(
        self,
        query: str,
        parameters: tuple = (),
    ):

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        self.connection.commit()

        return cursor

    # ---------------------------------------------------------
    # Fetch One
    # ---------------------------------------------------------

    def fetch_one(
        self,
        query: str,
        parameters: tuple = (),
    ):

        return self.execute(
            query,
            parameters,
        ).fetchone()

    # ---------------------------------------------------------
    # Fetch All
    # ---------------------------------------------------------

    def fetch_all(
        self,
        query: str,
        parameters: tuple = (),
    ):

        return self.execute(
            query,
            parameters,
        ).fetchall()

    # ---------------------------------------------------------
    # Schema
    # ---------------------------------------------------------

    def create_tables(self):

        # -------------------------------------------------
        # Trades
        # -------------------------------------------------

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

                status TEXT NOT NULL DEFAULT 'OPEN',

                opened TEXT NOT NULL,
                closed TEXT,

                exit_price REAL,
                profit_loss REAL DEFAULT 0
            )
            """
        )

        # -------------------------------------------------
        # Portfolio
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Journal
        # -------------------------------------------------

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS journal (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event TEXT NOT NULL,

                details TEXT,

                timestamp TEXT NOT NULL,

                symbol TEXT,

                direction TEXT,

                entry_price REAL,

                exit_price REAL,

                score INTEGER,

                confidence REAL,

                trend INTEGER,

                momentum INTEGER,

                volatility INTEGER,

                volume INTEGER,

                market_condition TEXT,

                outcome TEXT DEFAULT 'OPEN',

                profit_loss REAL DEFAULT 0,

                notes TEXT,

                created TEXT
            )
            """
        )

        # -------------------------------------------------
        # Equity History
        # -------------------------------------------------

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

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.connection.close()