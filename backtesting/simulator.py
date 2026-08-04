"""
Atlas AI Trading Platform 3.5

Backtesting Trade Simulator

Trade lifecycle engine.

Supports:

- Long trades
- Short trades
- ATR stop loss
- ATR targets
- Breakeven protection
- Maximum holding period
- Commission
- Slippage

Updated:

- Standardised result output
- Validation compatibility
- Optimisation compatibility
"""

from __future__ import annotations


from dataclasses import dataclass


from models.trade import Trade



@dataclass(slots=True)
class SimulatedTrade:


    symbol: str

    direction: str

    entry: float

    exit: float

    quantity: int

    profit_loss: float

    result: str

    candles_held: int



    entry_index: int = 0

    exit_index: int = 0




class Simulator:


    def __init__(
        self,
        starting_cash: float = 100000.0,
        commission: float = 1.0,
        slippage: float = 0.01,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
    ):


        self.starting_cash = starting_cash

        self.cash = starting_cash


        self.commission = commission

        self.slippage = slippage


        self.atr_stop = atr_stop

        self.atr_target = atr_target


        self.trades = []

        self.equity_curve = [

            starting_cash

        ]



    # =====================================================
    # SIMULATE TRADE
    # =====================================================

    def simulate_trade(
        self,
        trade: Trade,
        dataframe,
        index: int,
    ):


        entry = trade.entry


        atr = float(

            dataframe["ATR"].iloc[index]

        )


        if atr <= 0:

            atr = entry * 0.02



        stop_distance = (

            atr *

            self.atr_stop

        )


        target_distance = (

            atr *

            self.atr_target

        )



        if trade.direction == "LONG":


            stop_loss = entry - stop_distance

            take_profit = entry + target_distance



        else:


            stop_loss = entry + stop_distance

            take_profit = entry - target_distance




        breakeven_trigger = atr * 1.5


        breakeven_active = False


        exit_price = None


        candles_held = 0


        exit_index = index



        future = dataframe.iloc[index + 1:]



        for future_index, candle in future.iterrows():


            candles_held += 1


            high = float(

                candle["High"]

            )


            low = float(

                candle["Low"]

            )



            if trade.direction == "LONG":



                if high >= take_profit:


                    exit_price = take_profit

                    break



                if high >= entry + breakeven_trigger:


                    breakeven_active = True



                if low <= stop_loss:


                    exit_price = stop_loss

                    break



                if breakeven_active and low <= entry:


                    exit_price = entry

                    break



            else:



                if low <= take_profit:


                    exit_price = take_profit

                    break



                if low <= entry - breakeven_trigger:


                    breakeven_active = True



                if high >= stop_loss:


                    exit_price = stop_loss

                    break



                if breakeven_active and high >= entry:


                    exit_price = entry

                    break



            if candles_held >= 100:


                exit_price = float(

                    candle["Close"]

                )

                break



        if exit_price is None:


            exit_price = float(

                dataframe["Close"].iloc[-1]

            )



        if trade.direction == "LONG":


            exit_price -= self.slippage


        else:


            exit_price += self.slippage




        trade.close(

            exit_price

        )



        profit_loss = (

            trade.profit_loss

            -

            self.commission

        )



        simulated = SimulatedTrade(


            symbol=trade.symbol,


            direction=trade.direction,


            entry=round(

                entry,

                2

            ),


            exit=round(

                exit_price,

                2

            ),


            quantity=trade.quantity,


            profit_loss=round(

                profit_loss,

                2

            ),


            result=(

                "WIN"

                if profit_loss > 0

                else

                "LOSS"

            ),


            candles_held=candles_held,


            entry_index=index,

        )



        self.trades.append(

            simulated

        )


        self.cash += profit_loss



        self.equity_curve.append(

            self.cash

        )



        return simulated




    # =====================================================
    # RESULTS
    # =====================================================

    def results(self):


        wins = [

            trade

            for trade in self.trades

            if trade.profit_loss > 0

        ]


        losses = [

            trade

            for trade in self.trades

            if trade.profit_loss <= 0

        ]



        gross_profit = sum(

            trade.profit_loss

            for trade in wins

        )


        gross_loss = abs(

            sum(

                trade.profit_loss

                for trade in losses

            )

        )



        total = len(

            self.trades

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss > 0

            else 0

        )



        win_rate = (

            len(wins) / total * 100

            if total

            else 0

        )



        return {



            "starting_cash":

                round(

                    self.starting_cash,

                    2

                ),



            "ending_equity":

                round(

                    self.cash,

                    2

                ),



            "net_profit":

                round(

                    self.cash - self.starting_cash,

                    2

                ),



            "profit":

                round(

                    self.cash - self.starting_cash,

                    2

                ),



            "total_trades":

                total,



            "trades":

                total,



            "winning_trades":

                len(wins),



            "losing_trades":

                len(losses),



            "wins":

                len(wins),



            "losses":

                len(losses),



            "win_rate":

                round(

                    win_rate,

                    2

                ),



            "profit_factor":

                round(

                    profit_factor,

                    2

                ),



            "average_trade":

                round(

                    (

                        self.cash - self.starting_cash

                    )

                    /

                    total

                    if total

                    else 0,

                    2

                ),



            "max_drawdown":

                self.calculate_drawdown(),



        }




    # =====================================================
    # DRAW DOWN
    # =====================================================

    def calculate_drawdown(self):


        peak = self.equity_curve[0]


        max_drawdown = 0



        for value in self.equity_curve:


            if value > peak:

                peak = value



            drawdown = (

                (peak - value)

                /

                peak

                *

                100

            )



            if drawdown > max_drawdown:

                max_drawdown = drawdown



        return round(

            max_drawdown,

            2

        )