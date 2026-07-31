"""
Atlas AI Trading Platform 3.0

Paper Broker

Simulated execution environment.

Responsibilities:

- Submit orders
- Close orders
- Return positions
- Monitor open trades
"""

from __future__ import annotations


from brokers.base import Broker



class PaperBroker(Broker):
    """
    Paper trading broker implementation.
    """



    def __init__(
        self,
        trade_repository,
    ):

        self.trades = trade_repository



    # ==================================================
    # OPEN ORDER
    # ==================================================

    def submit_order(
        self,
        trade,
    ):

        self.trades.save(
            trade
        )

        return trade



    # ==================================================
    # CLOSE ORDER
    # ==================================================

    def close_order(
        self,
        trade,
        exit_price: float,
    ):

        self.trades.close_trade(

            trade,

            exit_price,

        )

        return trade



    # ==================================================
    # POSITIONS
    # ==================================================

    def get_positions(self):

        return self.trades.open_trades()



    # ==================================================
    # ACCOUNT
    # ==================================================

    def get_account(self):

        return {

            "type": "PAPER",

            "positions": len(

                self.get_positions()

            )

        }



    # ==================================================
    # TRADE MONITOR
    # ==================================================

    def monitor_open_trades(
        self,
        trades,
        prices,
    ):

        results = []


        for trade in trades:


            current_price = prices.get(

                trade.symbol

            )


            if current_price is None:

                continue



            result = self.check_trade(

                trade,

                current_price,

            )


            if result:

                results.append(

                    result

                )


        return results



    # ==================================================
    # STOP / TARGET CHECK
    # ==================================================

    def check_trade(
        self,
        trade,
        current_price,
    ):


        if trade.direction == "LONG":


            if current_price <= trade.stop_loss:

                return self.close_position(

                    trade,

                    current_price,

                    "STOP LOSS"

                )



            if current_price >= trade.take_profit:

                return self.close_position(

                    trade,

                    current_price,

                    "TAKE PROFIT"

                )



        else:


            if current_price >= trade.stop_loss:

                return self.close_position(

                    trade,

                    current_price,

                    "STOP LOSS"

                )



            if current_price <= trade.take_profit:

                return self.close_position(

                    trade,

                    current_price,

                    "TAKE PROFIT"

                )



        return None



    # ==================================================
    # CLOSE POSITION
    # ==================================================

    def close_position(
        self,
        trade,
        exit_price,
        reason,
    ):


        closed = self.close_order(

            trade,

            exit_price,

        )


        return {

            "symbol": closed.symbol,

            "direction": closed.direction,

            "exit_price": exit_price,

            "profit_loss": closed.profit_loss,

            "reason": reason,

        }