"""
Atlas AI Trading Platform

Signal Generator

Creates trading decisions from analysis scores.
"""

from __future__ import annotations

import pandas as pd

from models.scorecard import Scorecard

from scoring.trend_score import calculate_trend_score
from scoring.momentum_score import calculate_momentum_score
from scoring.volatility_score import calculate_volatility_score
from scoring.volume_score import calculate_volume_score



def generate_scorecard(
    df: pd.DataFrame,
) -> Scorecard:
    """
    Generate complete market scorecard.
    """

    trend = calculate_trend_score(
        df
    )

    momentum = calculate_momentum_score(
        df
    )

    volatility = calculate_volatility_score(
        df
    )

    volume = calculate_volume_score(
        df
    )


    score = Scorecard()


    score.trend = trend.score

    score.momentum = momentum.score

    score.volatility = volatility.score

    score.volume = volume.score


    # ---------------------------------
    # TOTAL SCORE
    # ---------------------------------

    score.total_score = (

        score.trend

        +
        score.momentum

        +
        score.volatility

        +
        score.volume

    )


    # ---------------------------------
    # MARKET BIAS
    # ---------------------------------

    if score.total_score >= 70:

        score.bullish = True

        score.signal = "BUY"


    elif score.total_score <= 30:

        score.bearish = True

        score.signal = "SELL"


    else:

        score.signal = "HOLD"



    # ---------------------------------
    # CONFIDENCE
    # ---------------------------------

    score.confidence = (

        abs(score.total_score)

        /
        100

    )


    return score




def explain_signal(
    df: pd.DataFrame,
) -> list[str]:
    """
    Returns reasons behind the signal.
    """

    trend = calculate_trend_score(
        df
    )

    momentum = calculate_momentum_score(
        df
    )

    volatility = calculate_volatility_score(
        df
    )

    volume = calculate_volume_score(
        df
    )


    reasons: list[str] = []


    reasons.extend(
        trend.reasons
    )

    reasons.extend(
        momentum.reasons
    )

    reasons.extend(
        volatility.reasons
    )

    reasons.extend(
        volume.reasons
    )


    return reasons