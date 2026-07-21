"""
Atlas AI Trading Assistant 2.0

Equity Curve
"""

from __future__ import annotations


class EquityCurve:

    def __init__(

        self,

        trade_repository,

        starting_balance=10000

    ):

        self.trades = trade_repository

        self.starting_balance = starting_balance


    def calculate(self):

        trades = self.trades.get_closed_trades()

        balance = self.starting_balance

        peak = balance

        max_drawdown = 0

        history = []


        for trade in trades:

            pnl = trade.profit_loss or 0.0

            balance += pnl

            peak = max(

                peak,

                balance

            )

            drawdown = peak - balance

            max_drawdown = max(

                max_drawdown,

                drawdown

            )

            history.append(

                {

                    "id": trade.id,

                    "symbol": trade.symbol,

                    "profit_loss": pnl,

                    "balance": round(

                        balance,

                        2

                    ),

                    "drawdown": round(

                        drawdown,

                        2

                    )

                }

            )


        return {

            "starting_balance": round(

                self.starting_balance,

                2

            ),

            "ending_balance": round(

                balance,

                2

            ),

            "peak_balance": round(

                peak,

                2

            ),

            "max_drawdown": round(

                max_drawdown,

                2

            ),

            "total_return": round(

                balance - self.starting_balance,

                2

            ),

            "history": history,

        }