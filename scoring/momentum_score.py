"""
Momentum Scoring
"""

from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class MomentumScore:
    score: int
    reasons: list[str]


def calculate_momentum_score(df: pd.DataFrame) -> MomentumScore:

    row = df.iloc[-1]

    score = 0
    reasons = []

    if row["RSI"] < 30:
        score += 15
        reasons.append("RSI Oversold")

    elif row["RSI"] > 70:
        score -= 15
        reasons.append("RSI Overbought")

    if row["MACD"] > row["MACD_SIGNAL"]:
        score += 15
        reasons.append("MACD Bullish")
    else:
        score -= 15
        reasons.append("MACD Bearish")

    if row["STOCH_K"] > row["STOCH_D"]:
        score += 10
        reasons.append("Stochastic Bullish")
    else:
        score -= 10
        reasons.append("Stochastic Bearish")

    return MomentumScore(score, reasons)