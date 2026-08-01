"""
Atlas AI Trading Platform 3.0

Optimisation Results Database

Stores optimisation experiments
and performance results.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime


class OptimisationDatabase:

    def __init__(
        self,
        path: str = "optimisation/results.db",
    ):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.path
        )

        self.create_tables()


    # ---------------------------------------------------------
    # Create tables
    # ---------------------------------------------------------

    def create_tables(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS optimisation_results (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT NOT NULL,

                score_threshold INTEGER,

                confidence REAL,

                atr_stop REAL,

                atr_target REAL,


                net_profit REAL,

                win_rate REAL,

                profit_factor REAL,

                total_trades INTEGER,


                ranking_score REAL,


                created TEXT

            )
            """
        )


        self.connection.commit()


    # ---------------------------------------------------------
    # Save result
    # ---------------------------------------------------------

    def save_result(
        self,
        symbol: str,
        result: dict,
    ):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            INSERT INTO optimisation_results (

                symbol,

                score_threshold,

                confidence,

                atr_stop,

                atr_target,


                net_profit,

                win_rate,

                profit_factor,

                total_trades,


                ranking_score,

                created

            )

            VALUES (?,?,?,?,?,?,?,?,?,?,?)

            """,

            (

                symbol,

                result["score_threshold"],

                result["confidence"],

                result["atr_stop"],

                result["atr_target"],


                result["net_profit"],

                result["win_rate"],

                result["profit_factor"],

                result["total_trades"],


                result["ranking_score"],


                datetime.now().isoformat(),

            ),
        )


        self.connection.commit()


    # ---------------------------------------------------------
    # Check existing configuration
    # ---------------------------------------------------------

    def exists(
        self,
        symbol: str,
        score_threshold: int,
        confidence: float,
        atr_stop: float,
        atr_target: float,
    ):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT id

            FROM optimisation_results

            WHERE

            symbol = ?

            AND score_threshold = ?

            AND confidence = ?

            AND atr_stop = ?

            AND atr_target = ?

            LIMIT 1

            """,

            (

                symbol,

                score_threshold,

                confidence,

                atr_stop,

                atr_target,

            ),
        )


        return cursor.fetchone() is not None


    # ---------------------------------------------------------
    # Best results
    # ---------------------------------------------------------

    def best_results(
        self,
        symbol: str | None = None,
        limit: int = 10,
    ):

        cursor = self.connection.cursor()


        if symbol:

            cursor.execute(
                """
                SELECT *

                FROM optimisation_results

                WHERE symbol = ?

                ORDER BY ranking_score DESC

                LIMIT ?

                """,

                (
                    symbol,
                    limit,
                ),
            )

        else:

            cursor.execute(
                """
                SELECT *

                FROM optimisation_results

                ORDER BY ranking_score DESC

                LIMIT ?

                """,

                (
                    limit,
                ),
            )


        return cursor.fetchall()