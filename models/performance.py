"""
Atlas AI Trading Platform

Performance Model

Represents complete account performance.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Performance:
    """
    Trading performance statistics.
    """

    # Account
    starting_balance: float = 10000.00
    current_balance: float = 10000.00
    peak_balance: float = 10000.00

    # Trades
    total_trades: int = 0
    open_trades: int = 0
    closed_trades: int = 0

    wins: int = 0
    losses: int = 0

    # Profit
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    net_profit: float = 0.0

    # Statistics
    average_win: float = 0.0
    average_loss: float = 0.0

    largest_win: float = 0.0
    largest_loss: float = 0.0

    profit_factor: float = 0.0
    expectancy: float = 0.0

    # Risk
    max_drawdown: float = 0.0
    current_drawdown: float = 0.0

    # Equity history
    equity_curve: list[float] = field(
        default_factory=list
    )

    @property
    def win_rate(self) -> float:

        if self.closed_trades == 0:
            return 0.0

        return round(

            (self.wins / self.closed_trades) * 100,

            2

        )

    @property
    def loss_rate(self) -> float:

        if self.closed_trades == 0:
            return 0.0

        return round(

            (self.losses / self.closed_trades) * 100,

            2

        )

    @property
    def return_percent(self) -> float:

        if self.starting_balance == 0:
            return 0.0

        return round(

            (
                self.net_profit
                /
                self.starting_balance
            ) * 100,

            2

        )

    def update_balance(
        self,
        balance: float
    ) -> None:
        """
        Update account balance.
        """

        self.current_balance = round(
            balance,
            2
        )

        if balance > self.peak_balance:

            self.peak_balance = round(
                balance,
                2
            )

        drawdown = (

            self.peak_balance
            -
            self.current_balance

        )

        if drawdown > self.max_drawdown:

            self.max_drawdown = round(
                drawdown,
                2
            )

        self.current_drawdown = round(
            drawdown,
            2
        )

        self.equity_curve.append(
            self.current_balance
        )

    def summary(self) -> dict:

        return {

            "starting_balance": self.starting_balance,

            "current_balance": self.current_balance,

            "peak_balance": self.peak_balance,

            "net_profit": self.net_profit,

            "gross_profit": self.gross_profit,

            "gross_loss": self.gross_loss,

            "wins": self.wins,

            "losses": self.losses,

            "total_trades": self.total_trades,

            "closed_trades": self.closed_trades,

            "open_trades": self.open_trades,

            "win_rate": self.win_rate,

            "loss_rate": self.loss_rate,

            "profit_factor": self.profit_factor,

            "expectancy": self.expectancy,

            "largest_win": self.largest_win,

            "largest_loss": self.largest_loss,

            "average_win": self.average_win,

            "average_loss": self.average_loss,

            "max_drawdown": self.max_drawdown,

            "current_drawdown": self.current_drawdown,

            "return_percent": self.return_percent,

        }

    def __str__(self):

        return (

            f"Performance("

            f"Balance=${self.current_balance:.2f}, "

            f"Net=${self.net_profit:.2f}, "

            f"Win Rate={self.win_rate:.2f}%"

            f")"

        )