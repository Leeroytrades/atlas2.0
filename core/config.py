"""
Atlas AI Trading Platform

Central Configuration

Single source of truth for
application settings.
"""

from __future__ import annotations





class Config:
    """
    Atlas application configuration.
    """



    # ==================================================
    # BROKER
    # ==================================================

    BROKER_MODE = "PAPER"



    # ==================================================
    # ACCOUNT
    # ==================================================

    ACCOUNT_SIZE = 10000.0


    RISK_PERCENT = 1.0



    # ==================================================
    # SCHEDULER
    # ==================================================

    SCHEDULER_INTERVAL = 60



    # ==================================================
    # MARKET
    # ==================================================

    MARKET_ENABLED = True


    MARKET_OPEN_HOUR = 9

    MARKET_OPEN_MINUTE = 30


    MARKET_CLOSE_HOUR = 16

    MARKET_CLOSE_MINUTE = 0



    # ==================================================
    # DATA
    # ==================================================

    DEFAULT_SYMBOLS = [

        "AAPL",

        "MSFT",

        "NVDA",

        "META",

        "AMZN",

        "GOOG",

        "TSLA",

        "AMD",

        "NFLX",

        "PLTR",

        "SPY",

        "QQQ",

    ]



    # ==================================================
    # TIMEFRAMES
    # ==================================================

    PRIMARY_TIMEFRAME = "5m"

    SECONDARY_TIMEFRAME = "15m"

    HIGHER_TIMEFRAME = "1h"



    # ==================================================
    # DATABASE
    # ==================================================

    DATABASE_FILE = "atlas.db"





# Backwards compatibility

BROKER_MODE = Config.BROKER_MODE