"""
Atlas AI Trading Platform 3.0

Market Scanner

Responsibilities:

- Scan active watchlist
- Request strategy analysis
- Build scan results
- Rank opportunities

Strategy logic belongs to StrategyService.
"""

from __future__ import annotations

from dataclasses import dataclass

from services.strategy_service import StrategyService


@dataclass(slots=True)
class ScanResult:
    """
    Result of analysing one symbol.
    """

    symbol: str

    dataframe: object

    score: int

    bias: str

    confidence: float

    scorecard: object | None = None


class Scanner:
    """
    Market scanner.

    Uses StrategyService for all analysis.
    """

    def __init__(self):

        self.strategy = StrategyService()


    def scan(
        self,
        symbols: list[str],
    ) -> list[ScanResult]:
        """
        Analyse a list of symbols.

        Returns:
            Ranked list of ScanResult objects
        """

        results: list[ScanResult] = []


        for symbol in symbols:

            try:

                scorecard, df = self.strategy.analyse(
                    symbol
                )


                results.append(

                    ScanResult(

                        symbol=symbol,

                        dataframe=df,

                        score=scorecard.total_score,

                        bias=scorecard.bias,

                        confidence=scorecard.confidence,

                        scorecard=scorecard,

                    )

                )


            except Exception as e:

                print(
                    f"{symbol}: {e}"
                )


        results.sort(

            key=lambda x: x.score,

            reverse=True,

        )


        return results