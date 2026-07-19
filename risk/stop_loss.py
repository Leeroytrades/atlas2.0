"""
ATR Stop Loss
"""

import pandas as pd


def calculate_stop_loss(
    df: pd.DataFrame,
    direction: str,
    atr_multiplier: float = 2.0,
) -> float:

    row = df.iloc[-1]

    atr = row["ATR"]

    close = row["Close"]

    if direction == "LONG":
        return close - atr * atr_multiplier

    return close + atr * atr_multiplier