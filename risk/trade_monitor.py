"""
Atlas AI Trading Assistant 2.1

Trade Monitor

Checks open positions against:
- Take Profit
- Stop Loss
"""

from __future__ import annotations

from datetime import datetime

from risk.trade_state import TradeState



class TradeMonitor:


    def __init__(

        self,

        trade_repository,

        journal=None

    ):

        self.trades = trade_repository

        self.journal = journal



    def check_trade(

        self,

        trade,

        current_price: float

    ):


        state = TradeState.OPEN



        # LONG trade

        if trade.direction == "LONG":


            if current_price >= trade.take_profit:

                state = TradeState.TARGET_HIT


            elif current_price <= trade.stop_loss:

                state = TradeState.STOPPED



        # SHORT trade

        elif trade.direction == "SHORT":


            if current_price <= trade.take_profit:

                state = TradeState.TARGET_HIT


            elif current_price >= trade.stop_loss:

                state = TradeState.STOPPED



        if state != TradeState.OPEN:


            profit_loss = (

                current_price - trade.entry

            ) * trade.quantity



            self.close_trade(

                trade,

                current_price,

                state,

                profit_loss

            )



        return state



    def close_trade(

        self,

        trade,

        exit_price,

        state,

        profit_loss

    ):


        self.trades.close_trade(

            trade.id,

            exit_price,

            profit_loss,

            datetime.now().isoformat()

        )



        if self.journal:


            self.journal.close_trade(

                trade.id,

                exit_price,

                profit_loss,

                state.value

            )