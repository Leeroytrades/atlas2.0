"""
Atlas AI Trading Assistant 2.2

Trade Monitor

Monitors open trades and closes them when
their stop loss or take profit is reached.
"""

from __future__ import annotations

from models.trade import Trade
from risk.trade_state import TradeState


class TradeMonitor:

    def __init__(
        self,
        trade_repository,
        journal=None,
    ):

        self.trades = trade_repository
        self.journal = journal

    # ---------------------------------------------------------
    # Check Trade
    # ---------------------------------------------------------

    def check_trade(
        self,
        trade: Trade,
        current_price: float,
    ) -> TradeState:

        state = TradeState.OPEN

        if trade.direction == "LONG":

            if current_price >= trade.take_profit:

                state = TradeState.TARGET_HIT

            elif current_price <= trade.stop_loss:

                state = TradeState.STOPPED

        else:

            if current_price <= trade.take_profit:

                state = TradeState.TARGET_HIT

            elif current_price >= trade.stop_loss:

                state = TradeState.STOPPED

        if state != TradeState.OPEN:

            self.close_trade(
                trade,
                current_price,
                state,
            )

        return state

    # ---------------------------------------------------------
    # Close Trade
    # ---------------------------------------------------------

    def close_trade(
        self,
        trade: Trade,
        exit_price: float,
        state: TradeState,
    ):

        closed_trade = self.trades.close_trade(
            trade,
            exit_price,
        )

        if self.journal:

            try:

                self.journal.close_trade(

                    closed_trade.id,

                    exit_price,

                    closed_trade.profit_loss,

                    state.value,

                )

            except Exception:

                # Journal failure should never stop
                # the trading engine.
                pass

        return closed_trade