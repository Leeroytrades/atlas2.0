"""
Atlas AI Trading Assistant 2.0

Volume Indicators
"""

from __future__ import annotations

import pandas as pd

from ta.volume import (
    OnBalanceVolumeIndicator,
    ChaikinMoneyFlowIndicator,
    VolumeWeightedAveragePrice,
)


def add_volume_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds volume-based indicators.
    """

    data = df.copy()

    # =========================
    # On Balance Volume
    # =========================

    obv = OnBalanceVolumeIndicator(
        close=data["Close"],
        volume=data["Volume"],
    )

    data["OBV"] = obv.on_balance_volume()

    # =========================
    # Chaikin Money Flow
    # =========================

    cmf = ChaikinMoneyFlowIndicator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        volume=data["Volume"],
        window=20,
    )

    data["CMF"] = cmf.chaikin_money_flow()

    # =========================
    # VWAP
    # =========================

    vwap = VolumeWeightedAveragePrice(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        volume=data["Volume"],
        window=14,
    )

    data["VWAP"] = vwap.volume_weighted_average_price()

    return data