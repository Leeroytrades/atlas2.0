"""
Atlas AI Trading Assistant 3.0

Volatility Indicators

Responsible for:

- ATR
- Bollinger Bands
- Bollinger Width

Trend indicators (ADX / DI) are intentionally NOT
calculated here. Those belong exclusively to
indicators.trend.
"""

from __future__ import annotations

import pandas as pd

from ta.volatility import (
    AverageTrueRange,
    BollingerBands,
)


def add_volatility_indicators(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Adds volatility indicators directly to the supplied
    DataFrame.

    Atlas 3.0 modifies the DataFrame in-place to reduce
    unnecessary DataFrame copies during optimisation and
    backtesting.
    """

    # =========================================================
    # Average True Range
    # =========================================================

    atr = AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14,
    )

    df["ATR"] = atr.average_true_range()

    # =========================================================
    # Bollinger Bands
    # =========================================================

    bb = BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2,
    )

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    df["BB_WIDTH"] = (
        (df["BB_UPPER"] - df["BB_LOWER"])
        / df["BB_MIDDLE"]
    )

    return df