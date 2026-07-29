"""
Atlas AI Trading Assistant 2.3

Backtesting Reports

Generates performance statistics
from simulated trades.
"""

from __future__ import annotations



class BacktestReport:


    def __init__(
        self,
        trades,
        starting_cash: float
    ):

        self.trades = trades

        self.starting_cash = starting_cash



    def generate(self):


        total = len(

            self.trades

        )


        wins = [

            trade

            for trade in self.trades

            if trade.profit_loss > 0

        ]


        losses = [

            trade

            for trade in self.trades

            if trade.profit_loss < 0

        ]



        gross_profit = sum(

            trade.profit_loss

            for trade in wins

        )



        gross_loss = abs(

            sum(

                trade.profit_loss

                for trade in losses

            )

        )



        net_profit = (

            gross_profit

            -

            gross_loss

        )



        win_rate = (

            len(wins)

            /

            total

            *

            100

            if total

            else 0

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss

            else float("inf")

        )



        ending_equity = (

            self.starting_cash

            +

            net_profit

        )



        return {


            "starting_cash":

                round(

                    self.starting_cash,

                    2

                ),


            "ending_equity":

                round(

                    ending_equity,

                    2

                ),


            "net_profit":

                round(

                    net_profit,

                    2

                ),


            "return_percent":

                round(

                    (

                        net_profit

                        /

                        self.starting_cash

                        *

                        100

                    )

                    if self.starting_cash

                    else 0,

                    2

                ),


            "total_trades":

                total,


            "wins":

                len(wins),


            "losses":

                len(losses),


            "win_rate":

                round(

                    win_rate,

                    2

                ),


            "profit_factor":

                round(

                    profit_factor,

                    2

                )

                if profit_factor != float("inf")

                else "INF"

        }