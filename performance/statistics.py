"""
Atlas AI Trading Assistant 2.0

Performance Statistics

Provides additional statistical analysis
for completed trades.
"""

from __future__ import annotations


class PerformanceStatistics:

    def __init__(self, trade_repository):

        self.trades = trade_repository


    def calculate(self):

        trades = self.trades.recent(100000)

        closed = [
            trade
            for trade in trades
            if trade["status"] == "CLOSED"
        ]

        if not closed:

            return {

                "best_trade": 0.0,

                "worst_trade": 0.0,

                "average_trade": 0.0,

                "average_risk_reward": 0.0,

                "total_closed": 0,

            }

        pnl = [

            trade["profit_loss"] or 0.0

            for trade in closed

        ]

        rr = [

            trade["risk_reward"] or 0.0

            for trade in closed

        ]

        return {

            "best_trade": round(
                max(pnl),
                2
            ),

            "worst_trade": round(
                min(pnl),
                2
            ),

            "average_trade": round(
                sum(pnl) / len(pnl),
                2
            ),

            "average_risk_reward": round(
                sum(rr) / len(rr),
                2
            ),

            "total_closed": len(closed),

        }