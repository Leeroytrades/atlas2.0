"""
Atlas AI Trading Assistant 2.3

Volatility & Trend Strength Indicators

Adds:

- ATR
- Bollinger Bands
- Bollinger Width
- ADX
- Positive Directional Indicator
- Negative Directional Indicator
"""

from __future__ import annotations

import pandas as pd

from ta.volatility import (
    AverageTrueRange,
    BollingerBands,
)

from ta.trend import ADXIndicator



def add_volatility_indicators(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Adds volatility and trend strength indicators.
    """

    data = df.copy()



    # ==========================
    # ATR
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


    data["BB_UPPER"] = (
        bb.bollinger_hband()
    )


    data["BB_MIDDLE"] = (
        bb.bollinger_mavg()
    )


    data["BB_LOWER"] = (
        bb.bollinger_lband()
    )


    data["BB_WIDTH"] = (

        (
            data["BB_UPPER"]
            -
            data["BB_LOWER"]
        )

        /

        data["BB_MIDDLE"]

    )



    # ==========================
    # ADX Trend Strength
    # ==========================

    adx = ADXIndicator(

        high=data["High"],

        low=data["Low"],

        close=data["Close"],

        window=14,

    )


    data["ADX"] = (
        adx.adx()
    )


    data["+DI"] = (
        adx.adx_pos()
    )


    data["-DI"] = (
        adx.adx_neg()
    )



    return data