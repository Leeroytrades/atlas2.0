"""
Atlas AI Trading Assistant 3.0

Momentum Indicators

Responsible for:

- RSI
- MACD
- MACD Signal
- MACD Histogram
- Stochastic %K
- Stochastic %D

Atlas 3.0 modifies the supplied DataFrame in-place to
avoid unnecessary DataFrame copies during research,
optimisation and backtesting.
"""

from __future__ import annotations

import pandas as pd

from ta.momentum import (
    RSIIndicator,
    StochasticOscillator,
)

from ta.trend import MACD


def add_momentum_indicators(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Adds momentum indicators directly to the supplied
    DataFrame.
    """

    # =========================================================
    # RSI
    # =========================================================

    rsi = RSIIndicator(
        close=df["Close"],
        window=14,
    )

    df["RSI"] = rsi.rsi()

    # =========================================================
    # MACD
    # =========================================================

    macd = MACD(
        close=df["Close"],
        window_fast=12,
        window_slow=26,
        window_sign=9,
    )

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    # =========================================================
    # Stochastic Oscillator
    # =========================================================

    stoch = StochasticOscillator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14,
        smooth_window=3,
    )

    df["STOCH_K"] = stoch.stoch()
    df["STOCH_D"] = stoch.stoch_signal()

    return df