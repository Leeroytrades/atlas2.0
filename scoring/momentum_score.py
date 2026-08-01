"""
Atlas AI Trading Platform 3.0

Momentum Scoring Engine

Uses:

- RSI recovery zones
- MACD momentum change
- Stochastic reversal
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd



@dataclass(slots=True)
class MomentumScore:

    score: int

    reasons: list[str]



def calculate_momentum_score(
    df: pd.DataFrame
) -> MomentumScore:


    row = df.iloc[-1]

    previous = df.iloc[-2]


    score = 0

    reasons = []



    rsi = float(
        row["RSI"]
    )


    previous_rsi = float(
        previous["RSI"]
    )


    macd = float(
        row["MACD"]
    )


    macd_signal = float(
        row["MACD_SIGNAL"]
    )


    previous_macd = float(
        previous["MACD"]
    )


    stoch_k = float(
        row["STOCH_K"]
    )


    stoch_d = float(
        row["STOCH_D"]
    )



    # =====================================================
    # RSI MOMENTUM
    #
    # Reward recovery
    # Avoid buying extremes
    # =====================================================


    if (

        45 <= rsi <= 60

        and

        rsi > previous_rsi

    ):

        score += 15

        reasons.append(
            "RSI recovering bullish momentum"
        )


    elif (

        40 <= rsi <= 55

        and

        rsi < previous_rsi

    ):

        score -= 15

        reasons.append(
            "RSI weakening bearish momentum"
        )


    elif rsi > 80:


        score -= 10

        reasons.append(
            "RSI extremely overbought"
        )


    elif rsi < 20:


        score += 10

        reasons.append(
            "RSI extremely oversold"
        )



    # =====================================================
    # MACD MOMENTUM CHANGE
    # =====================================================


    if (

        macd > macd_signal

        and

        macd > previous_macd

    ):

        score += 15

        reasons.append(
            "MACD momentum improving"
        )


    elif (

        macd < macd_signal

        and

        macd < previous_macd

    ):

        score -= 15

        reasons.append(
            "MACD momentum weakening"
        )



    # =====================================================
    # STOCHASTIC REVERSAL
    # =====================================================


    if (

        stoch_k > stoch_d

        and

        stoch_k < 80

    ):

        score += 10

        reasons.append(
            "Stochastic bullish reversal"
        )


    elif (

        stoch_k < stoch_d

        and

        stoch_k > 20

    ):

        score -= 10

        reasons.append(
            "Stochastic bearish reversal"
        )



    # =====================================================
    # NORMALISE
    # =====================================================

    score = max(

        min(score,40),

        -40

    )



    return MomentumScore(

        score,

        reasons

    )