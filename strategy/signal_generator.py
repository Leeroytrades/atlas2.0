"""
Atlas AI Trading Assistant 3.2

Optimised Signal Generator

Creates configurable trading signals.

Supports:

- Trend confirmation
- Momentum confirmation
- Volatility confirmation
- Volume confirmation
- EMA20 pullback filter
- Optimiser controlled thresholds

Optimised:
- Reduced dataframe duplication
- Faster repeated backtesting
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
    buy_threshold: int = 70,
) -> Scorecard:


    # ---------------------------------
    # Only evaluate latest candle
    # ---------------------------------

    row = df.iloc[-1:]


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



    score.total_score = (

        score.trend

        +

        score.momentum

        +

        score.volatility

        +

        score.volume

    )



    candle = row.iloc[0]



    adx = float(
        candle.get(
            "ADX",
            0
        )
    )


    di_plus = float(
        candle.get(
            "DI_PLUS",
            0
        )
    )


    di_minus = float(
        candle.get(
            "DI_MINUS",
            0
        )
    )


    rsi = float(
        candle.get(
            "RSI",
            50
        )
    )


    close = float(
        candle.get(
            "Close",
            0
        )
    )


    ema20 = float(
        candle.get(
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

        45 < rsi < 70

    )



    volatility_confirmed = (

        volatility.score >= 0

    )



    volume_confirmed = (

        volume.score >= 0

    )



    pullback_confirmed = (

        close <= ema20 * 1.02

    )



    if (

        score.total_score >= buy_threshold

        and trend_confirmed

        and momentum_confirmed

        and volatility_confirmed

        and volume_confirmed

        and pullback_confirmed

    ):


        score.bullish = True

        score.signal = "BUY"



    elif score.total_score <= -buy_threshold:


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


    reasons = []


    reasons.extend(
        calculate_trend_score(df).reasons
    )


    reasons.extend(
        calculate_momentum_score(df).reasons
    )


    reasons.extend(
        calculate_volatility_score(df).reasons
    )


    reasons.extend(
        calculate_volume_score(df).reasons
    )


    return reasons