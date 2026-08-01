"""
Atlas AI Trading Platform 3.0

Volume Scoring Engine

Uses:

- OBV momentum
- Chaikin Money Flow
- VWAP positioning
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd



@dataclass(slots=True)
class VolumeScore:

    score: int

    reasons: list[str]



def calculate_volume_score(
    df: pd.DataFrame
) -> VolumeScore:


    row = df.iloc[-1]

    previous = df.iloc[-5]


    score = 0

    reasons = []



    obv = float(
        row["OBV"]
    )


    previous_obv = float(
        previous["OBV"]
    )


    cmf = float(
        row["CMF"]
    )


    close = float(
        row["Close"]
    )


    vwap = float(
        row["VWAP"]
    )



    # =====================================================
    # OBV MOMENTUM
    # =====================================================


    if obv > previous_obv:

        score += 10

        reasons.append(
            "Increasing buying volume"
        )


    else:

        score -= 10

        reasons.append(
            "Decreasing buying volume"
        )



    # =====================================================
    # MONEY FLOW
    # =====================================================


    if cmf > 0.10:

        score += 10

        reasons.append(
            "Strong positive money flow"
        )


    elif cmf < -0.10:

        score -= 10

        reasons.append(
            "Strong negative money flow"
        )


    else:

        reasons.append(
            "Neutral money flow"
        )



    # =====================================================
    # VWAP POSITION
    #
    # Small weighting only
    # =====================================================


    distance = (

        (close - vwap)

        /

        vwap

    )



    if distance > 0.02:

        score += 5

        reasons.append(
            "Trading above VWAP"
        )


    elif distance < -0.02:

        score -= 5

        reasons.append(
            "Trading below VWAP"
        )



    score = max(

        min(score,25),

        -25

    )



    return VolumeScore(

        score,

        reasons

    )