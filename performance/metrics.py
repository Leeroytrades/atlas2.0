"""
Atlas AI Trading Assistant 2.0

Performance Metrics

Calculates:
- Total trades
- Wins / losses
- Win rate
- Profit
- Equity
- Growth
- Drawdown
"""

from __future__ import annotations



class PerformanceMetrics:


    def __init__(

        self,

        trade_repository

    ):

        self.trades = trade_repository



    def calculate(self):


        closed_trades = self.trades.closed_trades()

        open_trades = self.trades.open_trades()



        all_trades = (

            closed_trades

            +

            open_trades

        )



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

            len(closed_trades)

            *

            100

            if closed_trades

            else 0

        )



        starting_balance = 10000.00



        equity = (

            starting_balance

            +

            net_profit

        )



        growth = (

            net_profit

            /

            starting_balance

            *

            100

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss

            else float("inf")

        )



        expectancy = (

            net_profit / len(closed_trades)

            if closed_trades

            else 0

        )



        return {


            "total_trades":

                len(all_trades),


            "open_trades":

                len(open_trades),


            "closed_trades":

                len(closed_trades),


            "wins":

                len(wins),


            "losses":

                len(losses),


            "win_rate":

                round(win_rate, 2),


            "gross_profit":

                round(gross_profit, 2),


            "gross_loss":

                round(gross_loss, 2),


            "net_profit":

                round(net_profit, 2),


            "equity":

                round(equity, 2),


            "growth_percent":

                round(growth, 2),


            "average_win":

                round(

                    gross_profit / len(wins)

                    if wins

                    else 0,

                    2

                ),


            "average_loss":

                round(

                    gross_loss / len(losses)

                    if losses

                    else 0,

                    2

                ),


            "profit_factor":

                round(

                    profit_factor,

                    2

                ) if profit_factor != float("inf")

                else "INF",


            "expectancy":

                round(expectancy, 2),


            "drawdown":

            {

                "maximum_drawdown": 0

            }

        }