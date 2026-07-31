"""
Atlas AI Trading Platform 3.0

Backtesting Trade Simulator

Configurable:

- ATR stop loss
- ATR take profit
- Trailing stop
- Maximum holding period
- Commission
- Slippage
- Equity tracking
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


        self.trades: list[SimulatedTrade] = []


        self.equity_curve = [

            starting_cash

        ]





    def simulate_trade(
        self,
        trade: Trade,
        dataframe,
        index: int,
    ):


        entry = trade.entry



        try:

            atr = float(

                dataframe["ATR"].iloc[index]

            )

        except Exception:

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


            stop_loss = (

                entry

                -

                stop_distance

            )


            take_profit = (

                entry

                +

                target_distance

            )


        else:


            stop_loss = (

                entry

                +

                stop_distance

            )


            take_profit = (

                entry

                -

                target_distance

            )



        exit_price = None


        candles_held = 0


        highest_price = entry

        lowest_price = entry



        future = dataframe.iloc[

            index + 1:

        ]



        for _, candle in future.iterrows():


            candles_held += 1


            high = float(

                candle["High"]

            )


            low = float(

                candle["Low"]

            )



            if trade.direction == "LONG":


                if high > highest_price:

                    highest_price = high



                trailing_stop = (

                    highest_price

                    -

                    atr * 1.5

                )



                if low <= stop_loss:

                    exit_price = stop_loss

                    break



                if low <= trailing_stop:

                    exit_price = trailing_stop

                    break



                if high >= take_profit:

                    exit_price = take_profit

                    break



            else:


                if low < lowest_price:

                    lowest_price = low



                trailing_stop = (

                    lowest_price

                    +

                    atr * 1.5

                )



                if high >= stop_loss:

                    exit_price = stop_loss

                    break



                if high >= trailing_stop:

                    exit_price = trailing_stop

                    break



                if low <= take_profit:

                    exit_price = take_profit

                    break



            if candles_held >= 50:

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

            entry=round(entry,2),

            exit=round(exit_price,2),

            quantity=trade.quantity,

            profit_loss=round(profit_loss,2),

            result=(

                "WIN"

                if profit_loss > 0

                else "LOSS"

            ),

            candles_held=candles_held,

        )



        self.trades.append(

            simulated

        )


        self.cash += profit_loss


        self.equity_curve.append(

            self.cash

        )


        return simulated





    def results(self):


        wins = [

            t

            for t in self.trades

            if t.profit_loss > 0

        ]


        losses = [

            t

            for t in self.trades

            if t.profit_loss < 0

        ]



        gross_profit = sum(

            t.profit_loss

            for t in wins

        )


        gross_loss = abs(sum(

            t.profit_loss

            for t in losses

        ))



        total = len(

            self.trades

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss

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


            "total_trades":

                total,


            "wins":

                len(wins),


            "losses":

                len(losses),


            "win_rate":

                round(

                    len(wins)

                    /

                    total

                    *

                    100

                    if total

                    else 0,

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

                        self.cash

                        -

                        self.starting_cash

                    )

                    /

                    total

                    if total

                    else 0,

                    2

                )

        }