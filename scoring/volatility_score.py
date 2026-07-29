"""
Atlas AI Trading Assistant 2.3.1

Improved Volatility Scoring

Avoids penalising strong trends.
"""

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class VolatilityScore:

    score: int

    reasons: list[str]



def calculate_volatility_score(
    df: pd.DataFrame
) -> VolatilityScore:


    row = df.iloc[-1]


    score = 0

    reasons = []


    atr = row.get(
        "ATR",
        0
    )


    bb_width = row.get(
        "BB_WIDTH",
        0
    )


    #
    # Healthy volatility
    #

    if atr > 0:

        score += 5

        reasons.append(
            "Active volatility"
        )


    #
    # Avoid dead markets
    #

    if bb_width > 0.02:

        score += 5

        reasons.append(
            "Good price expansion"
        )


    return VolatilityScore(

        score,

        reasons

    )