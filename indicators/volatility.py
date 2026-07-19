"""
Atlas AI Trading Assistant 2.0

Volatility Indicators
"""

from __future__ import annotations

import pandas as pd

from ta.volatility import (
    AverageTrueRange,
    BollingerBands,
)


def add_volatility_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds volatility indicators.

    Indicators
    ----------
    ATR (14)

    Bollinger Bands (20)

    Upper Band
    Middle Band
    Lower Band

    Band Width
    """

    data = df.copy()

    # ==========================
    # Average True Range
    # ==========================

    atr = AverageTrueRange(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14,
    )

    data["ATR"] = atr.average_true_range()

    # ==========================
    # Bollinger Bands
    # ==========================

    bb = BollingerBands(
        close=data["Close"],
        window=20,
        window_dev=2,
    )

    data["BB_UPPER"] = bb.bollinger_hband()
    data["BB_MIDDLE"] = bb.bollinger_mavg()
    data["BB_LOWER"] = bb.bollinger_lband()

    data["BB_WIDTH"] = (
        data["BB_UPPER"] - data["BB_LOWER"]
    ) / data["BB_MIDDLE"]

    return data