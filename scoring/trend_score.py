"""
Atlas AI Trading Platform 3.0

Trend Scoring Engine

Uses:

- EMA alignment
- SMA alignment
- ADX strength
- Directional movement
- Pullback quality
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd



@dataclass(slots=True)
class TrendScore:

    score: int

    reasons: list[str]



def calculate_trend_score(
    df: pd.DataFrame
) -> TrendScore:


    row = df.iloc[-1]


    score = 0

    reasons = []



    close = float(row["Close"])

    ema20 = float(row["EMA_20"])

    ema50 = float(row["EMA_50"])

    sma20 = float(row["SMA_20"])

    sma50 = float(row["SMA_50"])

    adx = float(row["ADX"])

    di_plus = float(row["DI_PLUS"])

    di_minus = float(row["DI_MINUS"])



    # =====================================================
    # EMA TREND DIRECTION
    # =====================================================

    if ema20 > ema50:

        score += 25

        reasons.append(
            "EMA20 above EMA50 bullish trend"
        )

    else:

        score -= 25

        reasons.append(
            "EMA20 below EMA50 bearish trend"
        )



    # =====================================================
    # SMA TREND DIRECTION
    # =====================================================

    if sma20 > sma50:

        score += 15

        reasons.append(
            "SMA20 above SMA50"
        )

    else:

        score -= 15

        reasons.append(
            "SMA20 below SMA50"
        )



    # =====================================================
    # PULLBACK QUALITY
    #
    # Reward price near EMA20
    # Penalise chasing
    # =====================================================

    ema_distance = (

        (close - ema20)

        /

        ema20

    )



    if abs(ema_distance) <= 0.01:


        if close >= ema20:

            score += 15

            reasons.append(
                "Bullish EMA20 pullback entry"
            )

        else:

            score -= 15

            reasons.append(
                "Bearish EMA20 pullback entry"
            )


    elif ema_distance > 0.05:

        score -= 10

        reasons.append(
            "Price extended above EMA20"
        )


    elif ema_distance < -0.05:

        score += 10

        reasons.append(
            "Price extended below EMA20"
        )



    # =====================================================
    # ADX TREND STRENGTH
    # =====================================================

    if adx >= 25:


        if di_plus > di_minus:

            score += 20

            reasons.append(
                "Strong bullish ADX trend"
            )


        else:

            score -= 20

            reasons.append(
                "Strong bearish ADX trend"
            )


    else:

        reasons.append(
            "Weak trend strength"
        )



    # =====================================================
    # NORMALISE
    # =====================================================

    score = max(

        min(score,70),

        -70

    )



    return TrendScore(

        score,

        reasons

    )