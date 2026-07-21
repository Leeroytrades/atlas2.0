"""
Atlas AI Trading Platform

Trade Service
"""

from __future__ import annotations

from risk.risk_manager import create_trade


class TradeService:

    def create(
        self,
        symbol,
        df,
        score,
        account_balance,
    ):

        direction = "LONG"

        if score.bearish:

            direction = "SHORT"

        return create_trade(

            symbol=symbol,

            df=df,

            account_balance=account_balance,

            risk_percent=1.0,

            direction=direction,

            confidence=score.confidence,

        )