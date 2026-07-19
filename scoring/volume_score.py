"""
Volume Scoring
"""

from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class VolumeScore:
    score: int
    reasons: list[str]


def calculate_volume_score(df: pd.DataFrame) -> VolumeScore:

    row = df.iloc[-1]

    score = 0
    reasons = []

    if row["OBV"] > df["OBV"].iloc[-5]:
        score += 10
        reasons.append("OBV Rising")
    else:
        score -= 10
        reasons.append("OBV Falling")

    if row["CMF"] > 0:
        score += 10
        reasons.append("Positive Money Flow")
    else:
        score -= 10
        reasons.append("Negative Money Flow")

    if row["Close"] > row["VWAP"]:
        score += 5
        reasons.append("Above VWAP")
    else:
        score -= 5
        reasons.append("Below VWAP")

    return VolumeScore(score, reasons)