"""
Atlas AI Trading Platform 3.4

Validation Metrics

Calculates performance statistics
for walk-forward validation.

Updated:

- Stronger pass criteria
- Prevents low trade count false positives
- Improved stability scoring
- Regime validation support
"""

from __future__ import annotations

from dataclasses import dataclass



@dataclass
class ValidationMetrics:


    profit: float = 0.0

    win_rate: float = 0.0

    profit_factor: float = 0.0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    max_drawdown: float = 0.0

    stability_score: float = 0.0



    # =====================================================
    # CREATE FROM BACKTEST RESULT
    # =====================================================

    @classmethod
    def from_result(
        cls,
        result: dict,
    ):

        return cls(

            profit=result.get(
                "net_profit",
                result.get(
                    "profit",
                    0.0
                )
            ),


            win_rate=result.get(
                "win_rate",
                0.0
            ),


            profit_factor=result.get(
                "profit_factor",
                0.0
            ),


            total_trades=result.get(
                "total_trades",
                result.get(
                    "trades",
                    0
                )
            ),


            winning_trades=result.get(
                "winning_trades",
                0
            ),


            losing_trades=result.get(
                "losing_trades",
                0
            ),


            max_drawdown=result.get(
                "max_drawdown",
                0.0
            ),

        )



    # =====================================================
    # STABILITY SCORE
    # =====================================================

    def calculate_stability(
        self,
    ):

        score = 0



        # Profit

        if self.profit > 0:

            score += 35



        # Profit factor

        if self.profit_factor >= 3:

            score += 30

        elif self.profit_factor >= 2:

            score += 25

        elif self.profit_factor >= 1.5:

            score += 15

        elif self.profit_factor >= 1:

            score += 5



        # Trade sample size

        if self.total_trades >= 100:

            score += 20

        elif self.total_trades >= 50:

            score += 15

        elif self.total_trades >= 20:

            score += 10



        # Win rate

        if self.win_rate >= 60:

            score += 10

        elif self.win_rate >= 50:

            score += 5



        # Drawdown penalty

        if self.max_drawdown > 0:

            score -= min(

                self.max_drawdown * 0.5,

                20

            )



        self.stability_score = round(

            max(
                score,
                0
            ),

            2

        )


        return self.stability_score



    # =====================================================
    # VALIDATION PASS CHECK
    # =====================================================

    def passes(

        self,

        minimum_profit_factor: float = 1.5,

        minimum_trades: int = 20,

        minimum_win_rate: float = 45.0,

    ) -> bool:


        """
        Strong validation acceptance.

        Prevents:

        - 2 trade lucky wins
        - Huge fake profit factors
        - Overfitted windows

        """


        if self.profit <= 0:

            return False



        if self.total_trades < minimum_trades:

            return False



        if self.profit_factor < minimum_profit_factor:

            return False



        if self.win_rate < minimum_win_rate:

            return False



        return True



    # =====================================================
    # DICTIONARY EXPORT
    # =====================================================

    def to_dict(

        self,

    ) -> dict:


        return {


            "profit":

                self.profit,


            "win_rate":

                self.win_rate,


            "profit_factor":

                self.profit_factor,


            "total_trades":

                self.total_trades,


            "winning_trades":

                self.winning_trades,


            "losing_trades":

                self.losing_trades,


            "max_drawdown":

                self.max_drawdown,


            "stability_score":

                self.stability_score,

        }