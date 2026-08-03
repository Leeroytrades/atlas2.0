"""
Atlas AI Trading Platform 3.3

Validation Database

Stores walk-forward validation
experiments and results.
"""

from __future__ import annotations

import sqlite3

from datetime import datetime



class ValidationDatabase:


    def __init__(
        self,
        database="atlas.db",
    ):


        self.database = database

        self.create_tables()



    # =====================================================
    # Create Tables
    # =====================================================

    def create_tables(
        self,
    ):


        connection = sqlite3.connect(

            self.database

        )


        cursor = connection.cursor()



        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS validation_results (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                window_id INTEGER,

                training_profit REAL,

                training_pf REAL,

                training_win_rate REAL,

                validation_profit REAL,

                validation_pf REAL,

                validation_win_rate REAL,

                total_trades INTEGER,

                score_threshold INTEGER,

                confidence REAL,

                atr_stop REAL,

                atr_target REAL,

                verdict TEXT,

                created TEXT

            )
            """
        )



        connection.commit()

        connection.close()



    # =====================================================
    # Save Result
    # =====================================================

    def save(
        self,
        symbol: str,
        result: dict,
    ):


        connection = sqlite3.connect(

            self.database

        )


        cursor = connection.cursor()



        training = result.get(

            "training",

            {}

        )


        validation = result.get(

            "validation",

            {}

        )


        parameters = result.get(

            "parameters",

            {}

        )



        cursor.execute(
            """
            INSERT INTO validation_results (

                symbol,

                window_id,

                training_profit,

                training_pf,

                training_win_rate,

                validation_profit,

                validation_pf,

                validation_win_rate,

                total_trades,

                score_threshold,

                confidence,

                atr_stop,

                atr_target,

                verdict,

                created

            )

            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

            """,

            (

                symbol,

                result.get(
                    "window_id"
                ),

                training.get(
                    "profit",
                    0
                ),

                training.get(
                    "profit_factor",
                    0
                ),

                training.get(
                    "win_rate",
                    0
                ),

                validation.get(
                    "profit",
                    0
                ),

                validation.get(
                    "profit_factor",
                    0
                ),

                validation.get(
                    "win_rate",
                    0
                ),

                validation.get(
                    "total_trades",
                    0
                ),

                parameters.get(
                    "score_threshold"
                ),

                parameters.get(
                    "confidence"
                ),

                parameters.get(
                    "atr_stop"
                ),

                parameters.get(
                    "atr_target"
                ),

                result.get(
                    "verdict"
                ),

                datetime.now().isoformat(),

            )

        )



        connection.commit()

        connection.close()