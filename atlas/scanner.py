"""
Atlas Scanner
"""

from __future__ import annotations

from dataclasses import dataclass

from data.market_data import MarketData
from indicators.composite import build_indicator_set
from strategy.signal_generator import generate_scorecard


@dataclass(slots=True)
class ScanResult:

    symbol: str

    dataframe: object

    score: int

    bias: str

    confidence: float


class Scanner:

    def __init__(self):

        self.market = MarketData()

    def scan(
        self,
        symbols: list[str],
    ) -> list[ScanResult]:

        results: list[ScanResult] = []

        for symbol in symbols:

            try:

                df = self.market.get_history(symbol)

                df = build_indicator_set(df)

                scorecard = generate_scorecard(df)

                results.append(

                    ScanResult(

                        symbol=symbol,

                        dataframe=df,

                        score=scorecard.total_score,

                        bias=scorecard.bias,

                        confidence=scorecard.confidence,

                    )

                )

            except Exception as e:

                print(f"{symbol}: {e}")

        results.sort(

            key=lambda x: x.score,

            reverse=True,

        )

        return results