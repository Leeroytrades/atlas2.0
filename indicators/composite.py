"""
Atlas AI Trading Assistant 2.0

Composite Indicator Builder
"""

from __future__ import annotations

import pandas as pd

from indicators.trend import add_trend_indicators
from indicators.momentum import add_momentum_indicators
from indicators.volatility import add_volatility_indicators
from indicators.volume import add_volume_indicators


def build_indicator_set(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs every indicator module.

    Returns a DataFrame containing all indicators.
    """

    df = add_trend_indicators(df)

    df = add_momentum_indicators(df)

    df = add_volatility_indicators(df)

    df = add_volume_indicators(df)

    return df