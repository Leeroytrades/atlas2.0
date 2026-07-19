"""
Atlas AI Trading Assistant 2.0

Signal Generator
"""

from __future__ import annotations

import pandas as pd

from models.scorecard import Scorecard

from scoring.trend_score import calculate_trend_score
from scoring.momentum_score import calculate_momentum_score
from scoring.volatility_score import calculate_volatility_score
from scoring.volume_score import calculate_volume_score


def generate_scorecard(df: pd.DataFrame) -> Scorecard:
    """
    Generate a complete Bull/Bear scorecard.
    """

    trend = calculate_trend_score(df)
    momentum = calculate_momentum_score(df)
    volatility = calculate_volatility_score(df)
    volume = calculate_volume_score(df)

    score = Scorecard()

    score.trend = trend.score
    score.momentum = momentum.score
    score.volatility = volatility.score
    score.volume = volume.score

    score.confidence = abs(score.total_score) / 100

    return score


def explain_signal(df: pd.DataFrame) -> list[str]:
    """
    Returns every reason behind the generated score.
    """

    trend = calculate_trend_score(df)
    momentum = calculate_momentum_score(df)
    volatility = calculate_volatility_score(df)
    volume = calculate_volume_score(df)

    reasons: list[str] = []

    reasons.extend(trend.reasons)
    reasons.extend(momentum.reasons)
    reasons.extend(volatility.reasons)
    reasons.extend(volume.reasons)

    return reasons