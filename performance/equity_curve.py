"""
Atlas AI Trading Platform

Equity Curve System

Tracks:
- Account growth
- Balance history
- Trade impact
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.trade import Trade



@dataclass
class EquityPoint:
    """
    Single point on the equity curve.
    """

    trade_id: int | None

    timestamp: str

    equity: float



class EquityCurve:


    def __init__(
        self,
        starting_balance: float = 10000.00,
    ):

        self.starting_balance = starting_balance

        self.current_equity = starting_balance

        self.history: list[EquityPoint] = []



        self.history.append(

            EquityPoint(

                trade_id=None,

                timestamp="START",

                equity=starting_balance,

            )

        )



    def add_trade(
        self,
        trade: Trade,
    ):

        """
        Update equity after closed trade.
        """

        if trade.status != "CLOSED":

            return



        self.current_equity += trade.profit_loss



        self.history.append(

            EquityPoint(

                trade_id=trade.id,

                timestamp=(

                    trade.closed.isoformat()

                    if trade.closed

                    else ""

                ),

                equity=round(

                    self.current_equity,

                    2

                ),

            )

        )



    def value(
        self,
    ) -> float:

        return round(

            self.current_equity,

            2

        )



    def growth_percent(
        self,
    ) -> float:

        return round(

            (

                (

                    self.current_equity

                    -

                    self.starting_balance

                )

                /

                self.starting_balance

            )

            *

            100,

            2

        )



    def points(
        self,
    ) -> list[dict]:

        return [

            {

                "trade_id": point.trade_id,

                "timestamp": point.timestamp,

                "equity": point.equity,

            }

            for point in self.history

        ]