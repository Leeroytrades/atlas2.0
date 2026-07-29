"""
Atlas AI Trading Assistant 2.3.3

Signal Generator

Creates higher quality trading signals.

Adds:
- Trend confirmation
- Momentum confirmation
- Volatility confirmation
- Volume confirmation
- EMA20 pullback filter
"""

from __future__ import annotations

import pandas as pd

from models.scorecard import Scorecard

from scoring.trend_score import calculate_trend_score
from scoring.momentum_score import calculate_momentum_score
from scoring.volatility_score import calculate_volatility_score
from scoring.volume_score import calculate_volume_score



def generate_scorecard(
    df: pd.DataFrame
) -> Scorecard:


    trend = calculate_trend_score(df)

    momentum = calculate_momentum_score(df)

    volatility = calculate_volatility_score(df)

    volume = calculate_volume_score(df)



    score = Scorecard()



    score.trend = trend.score

    score.momentum = momentum.score

    score.volatility = volatility.score

    score.volume = volume.score



    score.total_score = (

        score.trend

        +

        score.momentum

        +

        score.volatility

        +

        score.volume

    )



    row = df.iloc[-1]



    adx = float(
        row.get(
            "ADX",
            0
        )
    )


    di_plus = float(
        row.get(
            "DI_PLUS",
            0
        )
    )


    di_minus = float(
        row.get(
            "DI_MINUS",
            0
        )
    )


    rsi = float(
        row.get(
            "RSI",
            50
        )
    )


    close = float(
        row.get(
            "Close",
            0
        )
    )


    ema20 = float(
        row.get(
            "EMA_20",
            close
        )
    )



    trend_confirmed = (

        adx >= 20

        and

        di_plus > di_minus

    )



    momentum_confirmed = (

        rsi > 45

        and

        rsi < 70

    )



    volatility_confirmed = (

        volatility.score >= 0

    )



    volume_confirmed = (

        volume.score >= 0

    )



    #
    # Prevent late entries
    # Only buy close to EMA20
    #

    pullback_confirmed = (

        close <= ema20 * 1.02

    )



    if (

        score.total_score >= 70

        and

        trend_confirmed

        and

        momentum_confirmed

        and

        volatility_confirmed

        and

        volume_confirmed

        and

        pullback_confirmed

    ):


        score.bullish = True

        score.signal = "BUY"



    elif score.total_score <= 30:


        score.bearish = True

        score.signal = "SELL"



    else:


        score.signal = "HOLD"



    score.confidence = min(

        abs(score.total_score) / 100,

        1.0

    )



    return score





def explain_signal(
    df: pd.DataFrame
) -> list[str]:


    trend = calculate_trend_score(df)

    momentum = calculate_momentum_score(df)

    volatility = calculate_volatility_score(df)

    volume = calculate_volume_score(df)



    reasons = []



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