"""
Atlas AI Trading Platform 3.5

Validation Metrics

Used for:

- Walk forward validation
- Robustness scoring
- Strategy acceptance
- Overfit protection
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
    # BUILD FROM BACKTEST RESULT
    # =====================================================

    @classmethod
    def from_result(
        cls,
        result: dict,
    ):


        return cls(

            profit=result.get(
                "profit",
                result.get(
                    "net_profit",
                    0
                )
            ),


            win_rate=result.get(
                "win_rate",
                0
            ),


            profit_factor=result.get(
                "profit_factor",
                0
            ),


            total_trades=result.get(
                "total_trades",
                0
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
                0
            ),


            stability_score=result.get(
                "stability_score",
                0
            ),

        )



    # =====================================================
    # ROBUSTNESS SCORE
    # =====================================================

    def robustness_score(self):


        score = 0



        # ---------------------------------
        # Profit
        # ---------------------------------

        if self.profit > 0:

            score += 25



        # ---------------------------------
        # Trade sample size
        # ---------------------------------

        if self.total_trades >= 100:

            score += 15


        elif self.total_trades >= 50:

            score += 10


        elif self.total_trades >= 30:

            score += 5



        # ---------------------------------
        # Profit factor
        # ---------------------------------

        if self.profit_factor >= 2:

            score += 25


        elif self.profit_factor >= 1.5:

            score += 15


        elif self.profit_factor >= 1:

            score += 5



        # ---------------------------------
        # Drawdown
        # ---------------------------------

        if self.max_drawdown <= 10:

            score += 20


        elif self.max_drawdown <= 15:

            score += 10


        elif self.max_drawdown > 25:

            score -= 40


        elif self.max_drawdown > 40:

            score -= 80



        # ---------------------------------
        # Stability
        # ---------------------------------

        if self.stability_score >= 80:

            score += 15


        elif self.stability_score >= 60:

            score += 10



        return max(

            0,

            min(

                score,

                100

            )

        )



    # =====================================================
    # PASS / FAIL
    # =====================================================

    def passes(self):


        score = self.robustness_score()



        # Hard safety checks

        if self.max_drawdown > 25:

            return False



        if self.profit_factor < 1.3:

            return False



        if self.total_trades < 30:

            return False



        return score >= 70



    # =====================================================
    # DICT OUTPUT
    # =====================================================

    def to_dict(
        self,
    ):


        return {


            "profit":

                round(
                    self.profit,
                    2
                ),


            "win_rate":

                round(
                    self.win_rate,
                    2
                ),


            "profit_factor":

                round(
                    self.profit_factor,
                    2
                ),


            "total_trades":

                self.total_trades,


            "winning_trades":

                self.winning_trades,


            "losing_trades":

                self.losing_trades,


            "max_drawdown":

                round(
                    self.max_drawdown,
                    2
                ),


            "stability_score":

                round(
                    self.stability_score,
                    2
                ),


            "robustness_score":

                self.robustness_score(),

        }