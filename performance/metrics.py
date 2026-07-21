"""
Atlas AI Trading Platform

Performance Metrics

Calculates:
- Trade statistics
- Win rate
- Profit factor
- Expectancy
- Equity
- Drawdown
"""

from __future__ import annotations

from performance.equity_curve import EquityCurve
from performance.drawdown import DrawdownCalculator



class PerformanceMetrics:


    def __init__(
        self,
        trade_repository,
        starting_balance: float = 10000.00,
    ):

        self.trades = trade_repository

        self.starting_balance = starting_balance

        self.equity_curve = EquityCurve(
            starting_balance
        )

        self.drawdown = DrawdownCalculator()



    def calculate(self):


        closed_trades = self.trades.closed_trades()



        wins = [

            trade

            for trade in closed_trades

            if trade.profit_loss > 0

        ]


        losses = [

            trade

            for trade in closed_trades

            if trade.profit_loss < 0

        ]



        self.equity_curve = EquityCurve(
            self.starting_balance
        )

        self.drawdown = DrawdownCalculator()



        for trade in closed_trades:

            self.equity_curve.add_trade(
                trade
            )

            self.drawdown.update(
                self.equity_curve.value()
            )



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



        total_closed = len(
            closed_trades
        )



        win_rate = (

            (len(wins) / total_closed) * 100

            if total_closed

            else 0

        )



        if gross_loss == 0:

            profit_factor = (

                "INF"

                if gross_profit > 0

                else 0

            )

        else:

            profit_factor = round(

                gross_profit / gross_loss,

                2

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

            )

            *

            average_win

            -

            (

                1 - (win_rate / 100)

            )

            *

            average_loss

        )



        return {


            "total_trades":

                len(self.trades.recent()),



            "open_trades":

                len(self.trades.open_trades()),



            "closed_trades":

                total_closed,



            "wins":

                len(wins),



            "losses":

                len(losses),



            "win_rate":

                round(
                    win_rate,
                    2
                ),



            "gross_profit":

                round(
                    gross_profit,
                    2
                ),



            "gross_loss":

                round(
                    gross_loss,
                    2
                ),



            "net_profit":

                round(
                    net_profit,
                    2
                ),



            "equity":

                self.equity_curve.value(),



            "growth_percent":

                self.equity_curve.growth_percent(),



            "drawdown":

                self.drawdown.summary(),



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

                profit_factor,



            "expectancy":

                round(
                    expectancy,
                    2
                ),

        }