"""
Atlas AI Trading Platform 3.0

Performance Service

Connects trade history to account analytics.

Responsibilities:

- Calculate account performance
- Track wins/losses
- Calculate profit statistics
- Update equity
"""

from __future__ import annotations


from models.performance import Performance



class PerformanceService:


    def __init__(
        self,
        trade_repository,
    ):

        self.trades = trade_repository



    def summary(self):

        performance = self.calculate()

        return performance.summary()



    def calculate(self):

        performance = Performance()



        open_trades = self.trades.open_trades()

        closed_trades = self.trades.closed_trades()



        # ------------------------------
        # Trade counts
        # ------------------------------

        performance.total_trades = (

            len(open_trades)

            +

            len(closed_trades)

        )


        performance.open_trades = len(
            open_trades
        )


        performance.closed_trades = len(
            closed_trades
        )



        # ------------------------------
        # Profit calculations
        # ------------------------------

        profits = []

        losses = []



        for trade in closed_trades:


            if trade.profit_loss > 0:

                profits.append(
                    trade.profit_loss
                )

            elif trade.profit_loss < 0:

                losses.append(
                    trade.profit_loss
                )



        performance.wins = len(
            profits
        )


        performance.losses = len(
            losses
        )



        performance.gross_profit = round(

            sum(profits),

            2

        )


        performance.gross_loss = round(

            abs(sum(losses)),

            2

        )


        performance.net_profit = round(

            performance.gross_profit
            -
            performance.gross_loss,

            2

        )



        # ------------------------------
        # Averages
        # ------------------------------

        if profits:

            performance.average_win = round(

                sum(profits) / len(profits),

                2

            )


            performance.largest_win = max(
                profits
            )



        if losses:

            performance.average_loss = round(

                abs(sum(losses)) / len(losses),

                2

            )


            performance.largest_loss = abs(

                min(losses)

            )



        # ------------------------------
        # Ratios
        # ------------------------------

        if performance.gross_loss > 0:

            performance.profit_factor = round(

                performance.gross_profit
                /
                performance.gross_loss,

                2

            )



        if performance.closed_trades > 0:

            win_probability = (

                performance.wins
                /
                performance.closed_trades

            )


            loss_probability = (

                performance.losses
                /
                performance.closed_trades

            )


            performance.expectancy = round(

                (
                    win_probability
                    *
                    performance.average_win
                )

                -

                (
                    loss_probability
                    *
                    performance.average_loss
                ),

                2

            )



        # ------------------------------
        # Equity
        # ------------------------------

        current_balance = (

            performance.starting_balance

            +

            performance.net_profit

        )


        performance.update_balance(

            current_balance

        )


        return performance