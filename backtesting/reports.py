"""
Atlas AI Trading Assistant 2.4

Advanced Backtest Reports

Calculates:
- Performance
- Risk
- Drawdown
- Expectancy
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

            t

            for t in self.trades

            if t.profit_loss > 0

        ]


        losses = [

            t

            for t in self.trades

            if t.profit_loss < 0

        ]



        gross_profit = sum(

            t.profit_loss

            for t in wins

        )


        gross_loss = abs(

            sum(

                t.profit_loss

                for t in losses

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



        average_win = (

            gross_profit / len(wins)

            if wins

            else 0

        )


        average_loss = (

            gross_loss / len(losses)

            if losses

            else 0

        )



        expectancy = (

            (

                win_rate / 100

                *

                average_win

            )

            -

            (

                (1 - win_rate / 100)

                *

                average_loss

            )

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss

            else 0

        )



        equity = self.starting_cash


        peak = equity

        max_drawdown = 0



        for trade in self.trades:


            equity += trade.profit_loss


            if equity > peak:

                peak = equity


            drawdown = peak - equity


            if drawdown > max_drawdown:

                max_drawdown = drawdown



        return {


            "starting_cash":

                round(
                    self.starting_cash,
                    2
                ),


            "ending_equity":

                round(
                    equity,
                    2
                ),


            "net_profit":

                round(
                    net_profit,
                    2
                ),


            "return_percent":

                round(

                    net_profit
                    /
                    self.starting_cash
                    *
                    100,

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


            "average_win":

                round(
                    average_win,
                    2
                ),


            "average_loss":

                round(
                    average_loss,
                    2
                ),


            "profit_factor":

                round(
                    profit_factor,
                    2
                ),


            "expectancy":

                round(
                    expectancy,
                    2
                ),


            "max_drawdown":

                round(
                    max_drawdown,
                    2
                )

        }