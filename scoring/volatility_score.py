"""
Volatility Scoring
"""

from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class VolatilityScore:
    score: int
    reasons: list[str]


def calculate_volatility_score(df: pd.DataFrame) -> VolatilityScore:

    row = df.iloc[-1]

    score = 0
    reasons = []

    if row["Close"] < row["BB_LOWER"]:
        score += 10
        reasons.append("Below lower Bollinger Band")

    elif row["Close"] > row["BB_UPPER"]:
        score -= 10
        reasons.append("Above upper Bollinger Band")

    return VolatilityScore(score, reasons)