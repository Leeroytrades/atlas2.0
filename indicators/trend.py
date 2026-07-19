"""
Atlas AI Trading Assistant

Trend Indicators

This module calculates trend-following technical indicators and appends them
to a pandas DataFrame.

Indicators
----------
- SMA 20
- SMA 50
- EMA 20
- EMA 50
- ADX
- +DI
- -DI
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
    Add trend indicators to a copy of the supplied DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the original data plus trend indicators.
    """

    data = df.copy()

    # -----------------------------
    # Simple Moving Averages
    # -----------------------------
    data["SMA_20"] = SMAIndicator(
        close=data["Close"],
        window=20,
    ).sma_indicator()

    data["SMA_50"] = SMAIndicator(
        close=data["Close"],
        window=50,
    ).sma_indicator()

    # -----------------------------
    # Exponential Moving Averages
    # -----------------------------
    data["EMA_20"] = EMAIndicator(
        close=data["Close"],
        window=20,
    ).ema_indicator()

    data["EMA_50"] = EMAIndicator(
        close=data["Close"],
        window=50,
    ).ema_indicator()

    # -----------------------------
    # Average Directional Index
    # -----------------------------
    adx = ADXIndicator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14,
    )

    data["ADX"] = adx.adx()
    data["DI_PLUS"] = adx.adx_pos()
    data["DI_MINUS"] = adx.adx_neg()

    return data