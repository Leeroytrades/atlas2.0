"""
Atlas AI Trading Assistant 2.0

Performance Metrics

Calculates:
- Total trades
- Closed trades
- Wins
- Losses
- Win rate
- Profit / Loss
- Average win
- Average loss
- Profit factor
"""

from __future__ import annotations



class PerformanceMetrics:


    def __init__(
        self,
        trade_repository
    ):

        self.trades = trade_repository



    def calculate(self):

        trades = self.trades.recent(
            1000
        )


        closed = [

            trade

            for trade in trades

            if trade["status"] == "CLOSED"

        ]


        wins = [

            trade

            for trade in closed

            if trade["profit_loss"] > 0

        ]


        losses = [

            trade

            for trade in closed

            if trade["profit_loss"] < 0

        ]



        total_profit = sum(

            trade["profit_loss"]

            for trade in closed

            if trade["profit_loss"]

        )



        average_win = (

            sum(
                trade["profit_loss"]
                for trade in wins
            )
            /
            len(wins)

            if wins

            else 0

        )



        average_loss = (

            sum(
                trade["profit_loss"]
                for trade in losses
            )
            /
            len(losses)

            if losses

            else 0

        )



        profit_factor = (

            abs(
                sum(
                    trade["profit_loss"]
                    for trade in wins
                )
            )
            /
            abs(
                sum(
                    trade["profit_loss"]
                    for trade in losses
                )
            )

            if losses

            else 0

        )



        win_rate = (

            len(wins)
            /
            len(closed)

            if closed

            else 0

        )



        return {

            "total_trades": len(trades),

            "closed_trades": len(closed),

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": win_rate,

            "total_profit_loss": total_profit,

            "average_win": average_win,

            "average_loss": average_loss,

            "profit_factor": profit_factor,

        }