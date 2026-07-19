"""
Atlas AI Trading Assistant 2.0

Momentum Indicators
"""

from __future__ import annotations

import pandas as pd

from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD


def add_momentum_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds momentum indicators to a DataFrame.

    Indicators:
        - RSI (14)
        - MACD
        - MACD Signal
        - MACD Histogram
        - Stochastic %K
        - Stochastic %D
    """

    data = df.copy()

    # RSI
    rsi = RSIIndicator(
        close=data["Close"],
        window=14,
    )

    data["RSI"] = rsi.rsi()

    # MACD
    macd = MACD(
        close=data["Close"],
        window_fast=12,
        window_slow=26,
        window_sign=9,
    )

    data["MACD"] = macd.macd()
    data["MACD_SIGNAL"] = macd.macd_signal()
    data["MACD_HIST"] = macd.macd_diff()

    # Stochastic Oscillator
    stoch = StochasticOscillator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14,
        smooth_window=3,
    )

    data["STOCH_K"] = stoch.stoch()
    data["STOCH_D"] = stoch.stoch_signal()

    return data