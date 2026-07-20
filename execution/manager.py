"""
Atlas AI Trading Assistant 2.0

Execution Manager

Controls:
- Open trade monitoring
- Stop loss detection
- Take profit detection
- Trade closing
- P/L calculation
"""

from __future__ import annotations



class ExecutionManager:


    def __init__(
        self,
        trade_repository
    ):

        self.trades = trade_repository



    def monitor_open_trades(
        self,
        trades,
        prices
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
                current_price
            )


            if result:

                results.append(
                    result
                )


        return results



    def check_trade(
        self,
        trade,
        current_price
    ):


        if trade.direction == "LONG":


            if current_price <= trade.stop_loss:

                return self.close_trade(
                    trade,
                    current_price,
                    "STOP LOSS"
                )


            if current_price >= trade.take_profit:

                return self.close_trade(
                    trade,
                    current_price,
                    "TAKE PROFIT"
                )



        else:


            if current_price >= trade.stop_loss:

                return self.close_trade(
                    trade,
                    current_price,
                    "STOP LOSS"
                )


            if current_price <= trade.take_profit:

                return self.close_trade(
                    trade,
                    current_price,
                    "TAKE PROFIT"
                )



        return None



    def close_trade(
        self,
        trade,
        exit_price,
        reason
    ):


        closed_trade = self.trades.close_trade(
            trade,
            exit_price
        )


        return {

            "symbol": closed_trade.symbol,

            "direction": closed_trade.direction,

            "exit_price": exit_price,

            "profit_loss": closed_trade.profit_loss,

            "reason": reason,

        }