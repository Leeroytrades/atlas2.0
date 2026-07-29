"""
Atlas AI Trading Assistant 2.3

Trend Scoring Engine

Uses:

- EMA alignment
- SMA trend
- ADX strength
- Directional movement
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



    close = float(
        row["Close"]
    )


    ema20 = float(
        row["EMA_20"]
    )


    ema50 = float(
        row["EMA_50"]
    )


    sma20 = float(
        row["SMA_20"]
    )


    sma50 = float(
        row["SMA_50"]
    )


    adx = float(
        row["ADX"]
    )


    di_plus = float(
        row["DI_PLUS"]
    )


    di_minus = float(
        row["DI_MINUS"]
    )



    # -------------------------
    # EMA TREND
    # -------------------------

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



    # -------------------------
    # SMA TREND
    # -------------------------

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



    # -------------------------
    # PRICE POSITION
    # -------------------------

    if close > ema20:

        score += 10

        reasons.append(
            "Price above EMA20"
        )


    else:

        score -= 10

        reasons.append(
            "Price below EMA20"
        )



    # -------------------------
    # ADX TREND STRENGTH
    # -------------------------

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



    # -------------------------
    # NORMALISE
    # -------------------------

    score = max(
        min(score,70),
        -70
    )


    return TrendScore(

        score,

        reasons

    )