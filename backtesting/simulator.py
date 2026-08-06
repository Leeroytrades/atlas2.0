"""
Atlas AI Trading Platform 4.0

Backtesting Trade Simulator

Trade lifecycle engine.

Supports:

- Long trades
- Short trades
- ATR stops
- ATR targets
- Breakeven protection
- Maximum holding period
- Commission
- Slippage
- Strategy attribution
- Exit reason tracking

"""

from __future__ import annotations


from dataclasses import dataclass, field

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


    strategy: str = "UNKNOWN"

    exit_reason: str = "UNKNOWN"

    risk_reward: float = 0.0




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




    def simulate_trade(

        self,

        trade: Trade,

        dataframe,

        index: int,

    ):


        entry = float(trade.entry)



        atr = float(

            dataframe["ATR"].iloc[index]

        )


        if atr <= 0:

            atr = entry * 0.02



        stop_distance = atr * self.atr_stop

        target_distance = atr * self.atr_target



        if trade.direction == "LONG":


            stop_loss = entry - stop_distance

            take_profit = entry + target_distance


        else:


            stop_loss = entry + stop_distance

            take_profit = entry - target_distance




        risk_reward = (

            target_distance /

            stop_distance

        )




        breakeven_trigger = atr * 1.5


        breakeven_active = False



        exit_price = None

        exit_reason = "END_OF_DATA"


        exit_position = index


        candles_held = 0




        future = dataframe.iloc[index + 1:]




        for future_position, (future_index, candle) in enumerate(

            future.iterrows(),

            start=index + 1

        ):


            candles_held += 1


            exit_position = future_position



            high = float(candle["High"])

            low = float(candle["Low"])




            if trade.direction == "LONG":



                if high >= take_profit:


                    exit_price = take_profit

                    exit_reason = "TARGET"

                    break



                if high >= entry + breakeven_trigger:


                    breakeven_active = True




                if breakeven_active and low <= entry:


                    exit_price = entry

                    exit_reason = "BREAKEVEN"

                    break




                if low <= stop_loss:


                    exit_price = stop_loss

                    exit_reason = "STOP"

                    break




            else:



                if low <= take_profit:


                    exit_price = take_profit

                    exit_reason = "TARGET"

                    break




                if low <= entry - breakeven_trigger:


                    breakeven_active = True




                if breakeven_active and high >= entry:


                    exit_price = entry

                    exit_reason = "BREAKEVEN"

                    break




                if high >= stop_loss:


                    exit_price = stop_loss

                    exit_reason = "STOP"

                    break




            if candles_held >= 100:


                exit_price = float(

                    candle["Close"]

                )


                exit_reason = "MAX_HOLD"

                break





        if exit_price is None:


            exit_price = float(

                dataframe["Close"].iloc[-1]

            )


            exit_position = len(dataframe)-1

            exit_reason = "END_OF_DATA"





        if trade.direction == "LONG":


            exit_price -= self.slippage


        else:


            exit_price += self.slippage




        trade.close(exit_price)




        profit_loss = (

            trade.profit_loss

            -

            self.commission

        )




        strategy = getattr(

            trade,

            "strategy",

            "UNKNOWN"

        )




        simulated = SimulatedTrade(


            symbol=trade.symbol,


            direction=trade.direction,


            entry=round(entry,2),


            exit=round(exit_price,2),


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

                if profit_loss < 0

                else

                "BREAKEVEN"

            ),


            candles_held=candles_held,


            entry_index=index,


            exit_index=exit_position,


            strategy=strategy,


            exit_reason=exit_reason,


            risk_reward=round(

                risk_reward,

                2

            ),

        )




        self.trades.append(simulated)



        self.cash += profit_loss




        self.equity_curve.append(

            self.cash

        )



        return simulated





    def results(self):


        wins = [

            t for t in self.trades

            if t.profit_loss > 0

        ]


        losses = [

            t for t in self.trades

            if t.profit_loss < 0

        ]



        gross_profit = sum(

            t.profit_loss

            for t in wins

        )



        gross_loss = abs(

            sum(

                t.profit_loss

                for t in losses

            )

        )



        total = len(self.trades)



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss > 0

            else 0

        )



        win_rate = (

            len(wins)

            /

            total

            *

            100

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

                    self.cash -

                    self.starting_cash,

                    2

                ),



            "profit":

                round(

                    self.cash -

                    self.starting_cash,

                    2

                ),



            "total_trades":

                total,



            "trades":

                total,



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

                        self.cash -

                        self.starting_cash

                    )

                    /

                    total

                    if total

                    else 0,

                    2

                ),



            "max_drawdown":

                self.calculate_drawdown(),



            "trade_list":

                self.trades,

        }





    def calculate_drawdown(self):


        peak = self.equity_curve[0]


        max_drawdown = 0



        for value in self.equity_curve:


            if value > peak:

                peak = value



            drawdown = (

                (peak-value)

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