"""
Atlas AI Trading Assistant 3.0

Volume Indicators

Responsible for:

- On Balance Volume
- Chaikin Money Flow
- VWAP

Atlas 3.0 modifies the supplied DataFrame in-place to
avoid unnecessary DataFrame copies during research,
optimisation and backtesting.
"""

from __future__ import annotations

import pandas as pd

from ta.volume import (
    OnBalanceVolumeIndicator,
    ChaikinMoneyFlowIndicator,
    VolumeWeightedAveragePrice,
)


def add_volume_indicators(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Adds volume indicators directly to the supplied
    DataFrame.
    """

    # =========================================================
    # On Balance Volume
    # =========================================================

    obv = OnBalanceVolumeIndicator(
        close=df["Close"],
        volume=df["Volume"],
    )

    df["OBV"] = obv.on_balance_volume()

    # =========================================================
    # Chaikin Money Flow
    # =========================================================

    cmf = ChaikinMoneyFlowIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        volume=df["Volume"],
        window=20,
    )

    df["CMF"] = cmf.chaikin_money_flow()

    # =========================================================
    # VWAP
    # =========================================================

    vwap = VolumeWeightedAveragePrice(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        volume=df["Volume"],
        window=14,
    )

    df["VWAP"] = vwap.volume_weighted_average_price()

    return df