"""
Atlas AI Trading Assistant 2.0

Performance Metrics

Calculates overall trading statistics.
"""

from __future__ import annotations


class PerformanceMetrics:

    def __init__(self, trade_repository):

        self.trades = trade_repository

    def calculate(self):

        trades = self.trades.recent(100000)

        total = len(trades)

        open_trades = 0
        closed_trades = 0

        wins = 0
        losses = 0

        gross_profit = 0.0
        gross_loss = 0.0

        largest_win = 0.0
        largest_loss = 0.0

        for trade in trades:

            status = trade["status"]

            if status == "OPEN":
                open_trades += 1
                continue

            closed_trades += 1

            pnl = trade["profit_loss"] or 0.0

            if pnl >= 0:

                wins += 1

                gross_profit += pnl

                largest_win = max(
                    largest_win,
                    pnl
                )

            else:

                losses += 1

                gross_loss += abs(pnl)

                largest_loss = min(
                    largest_loss,
                    pnl
                )

        win_rate = 0.0

        if closed_trades:

            win_rate = (
                wins / closed_trades
            ) * 100

        average_win = (
            gross_profit / wins
            if wins
            else 0.0
        )

        average_loss = (
            gross_loss / losses
            if losses
            else 0.0
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss
            else 0.0
        )

        net_profit = (
            gross_profit - gross_loss
        )

        expectancy = 0.0

        if closed_trades:

            expectancy = (
                net_profit /
                closed_trades
            )

        return {

            "total_trades": total,

            "open_trades": open_trades,

            "closed_trades": closed_trades,

            "wins": wins,

            "losses": losses,

            "win_rate": round(
                win_rate,
                2
            ),

            "gross_profit": round(
                gross_profit,
                2
            ),

            "gross_loss": round(
                gross_loss,
                2
            ),

            "net_profit": round(
                net_profit,
                2
            ),

            "average_win": round(
                average_win,
                2
            ),

            "average_loss": round(
                average_loss,
                2
            ),

            "largest_win": round(
                largest_win,
                2
            ),

            "largest_loss": round(
                largest_loss,
                2
            ),

            "profit_factor": round(
                profit_factor,
                2
            ),

            "expectancy": round(
                expectancy,
                2
            ),

        }