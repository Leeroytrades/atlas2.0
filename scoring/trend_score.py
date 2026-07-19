"""
Atlas AI Trading Assistant 2.0

Trend Scoring
"""

from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class TrendScore:
    score: int
    reasons: list[str]


def calculate_trend_score(df: pd.DataFrame) -> TrendScore:

    row = df.iloc[-1]

    score = 0
    reasons = []

    if row["EMA_20"] > row["EMA_50"]:
        score += 15
        reasons.append("EMA20 above EMA50")
    else:
        score -= 15
        reasons.append("EMA20 below EMA50")

    if row["SMA_20"] > row["SMA_50"]:
        score += 15
        reasons.append("SMA20 above SMA50")
    else:
        score -= 15
        reasons.append("SMA20 below SMA50")

    if row["ADX"] > 25:

        if row["DI_PLUS"] > row["DI_MINUS"]:
            score += 10
            reasons.append("Strong uptrend")
        else:
            score -= 10
            reasons.append("Strong downtrend")

    return TrendScore(score, reasons)