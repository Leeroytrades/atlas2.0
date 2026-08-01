"""
Atlas AI Trading Assistant 3.0

Trend Indicators

Responsible for:

- SMA 20
- SMA 50
- EMA 20
- EMA 50
- ADX
- DI_PLUS
- DI_MINUS

This module is the single source of truth for
trend-related indicators.
"""

from __future__ import annotations

import pandas as pd

from ta.trend import (
    SMAIndicator,
    EMAIndicator,
    ADXIndicator,
)


def add_trend_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds trend indicators directly to the supplied DataFrame.

    Notes
    -----
    Atlas 3.0 modifies the DataFrame in-place to avoid
    unnecessary DataFrame copies during research,
    optimisation and backtesting.
    """

    # ---------------------------------------------------------
    # Moving Averages
    # ---------------------------------------------------------

    df["SMA_20"] = SMAIndicator(
        close=df["Close"],
        window=20,
    ).sma_indicator()

    df["SMA_50"] = SMAIndicator(
        close=df["Close"],
        window=50,
    ).sma_indicator()

    df["EMA_20"] = EMAIndicator(
        close=df["Close"],
        window=20,
    ).ema_indicator()

    df["EMA_50"] = EMAIndicator(
        close=df["Close"],
        window=50,
    ).ema_indicator()

    # ---------------------------------------------------------
    # ADX + Directional Movement
    # ---------------------------------------------------------

    adx = ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14,
    )

    df["ADX"] = adx.adx()
    df["DI_PLUS"] = adx.adx_pos()
    df["DI_MINUS"] = adx.adx_neg()

    return df