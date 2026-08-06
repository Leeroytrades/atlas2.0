"""
Atlas AI Trading Platform 3.6

Validation Metrics

Used for:

- Walk forward validation
- Robustness scoring
- Strategy acceptance
- Overfit protection

Updated:

- Correct profit factor calculation
- Trade aggregation support
- Optimisation compatibility
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


        trades = result.get(
            "trade_list",
            result.get(
                "trades",
                []
            )
        )


        winning = 0

        losing = 0

        gross_profit = 0.0

        gross_loss = 0.0



        # ---------------------------------
        # Calculate from trades if available
        # ---------------------------------

        if isinstance(
            trades,
            list
        ):


            for trade in trades:


                if isinstance(
                    trade,
                    dict
                ):

                    pnl = trade.get(
                        "profit_loss",
                        trade.get(
                            "pnl",
                            0
                        )
                    )


                else:

                    pnl = getattr(
                        trade,
                        "profit_loss",
                        0
                    )



                try:

                    pnl = float(
                        pnl
                    )

                except:

                    pnl = 0



                if pnl > 0:

                    winning += 1

                    gross_profit += pnl


                elif pnl < 0:

                    losing += 1

                    gross_loss += abs(
                        pnl
                    )



            total = winning + losing


            if total:

                win_rate = (

                    winning

                    /

                    total

                    *

                    100

                )


            else:

                win_rate = 0



            profit_factor = (

                gross_profit / gross_loss

                if gross_loss > 0

                else 0

            )


        else:


            total = result.get(

                "total_trades",

                result.get(

                    "trades",

                    0

                )

            )


            winning = result.get(

                "winning_trades",

                result.get(

                    "wins",

                    0

                )

            )


            losing = result.get(

                "losing_trades",

                result.get(

                    "losses",

                    0

                )

            )


            win_rate = result.get(

                "win_rate",

                0

            )


            profit_factor = result.get(

                "profit_factor",

                0

            )



        profit = result.get(

            "profit",

            result.get(

                "net_profit",

                0

            )

        )



        return cls(

            profit=float(
                profit
            ),

            win_rate=float(
                win_rate
            ),

            profit_factor=float(
                profit_factor
            ),

            total_trades=int(
                total
            ),

            winning_trades=int(
                winning
            ),

            losing_trades=int(
                losing
            ),

            max_drawdown=float(

                result.get(

                    "max_drawdown",

                    0

                )

            ),

            stability_score=float(

                result.get(

                    "stability_score",

                    0

                )

            ),

        )



    # =====================================================
    # ROBUSTNESS SCORE
    # =====================================================

    def robustness_score(
        self,
    ):


        score = 0



        # Profit

        if self.profit > 0:

            score += 25



        # Sample size

        if self.total_trades >= 100:

            score += 15


        elif self.total_trades >= 50:

            score += 10


        elif self.total_trades >= 30:

            score += 5



        # Profit factor

        if self.profit_factor >= 3:

            score += 25


        elif self.profit_factor >= 2:

            score += 20


        elif self.profit_factor >= 1.5:

            score += 15


        elif self.profit_factor >= 1:

            score += 5



        # Drawdown

        if self.max_drawdown <= 10:

            score += 20


        elif self.max_drawdown <= 15:

            score += 10


        elif self.max_drawdown > 25:

            score -= 40



        # Stability

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

    def passes(
        self,
    ):


        score = self.robustness_score()



        if self.max_drawdown > 25:

            return False



        if self.profit_factor < 1.3:

            return False



        if self.total_trades < 30:

            return False



        return score >= 70



    # =====================================================
    # OUTPUT
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