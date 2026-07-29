"""
Atlas AI Trading Assistant 2.3

Backtesting Trade Simulator

Converts Atlas strategy signals into
simulated trades and equity results.
"""

from __future__ import annotations

from dataclasses import dataclass



@dataclass(slots=True)
class SimulatedTrade:

    symbol: str

    direction: str

    entry: float

    exit: float

    profit_loss: float

    result: str



class Simulator:


    def __init__(
        self,
        starting_cash: float = 100000.0
    ):

        self.starting_cash = starting_cash

        self.cash = starting_cash

        self.trades = []

        self.equity_curve = [

            starting_cash

        ]



    def execute(
        self,
        symbol: str,
        price: float,
        direction: str,
        future_price: float
    ):


        if direction == "LONG":

            pnl = future_price - price


        elif direction == "SHORT":

            pnl = price - future_price


        else:

            return None



        trade = SimulatedTrade(

            symbol=symbol,

            direction=direction,

            entry=round(price, 2),

            exit=round(future_price, 2),

            profit_loss=round(pnl, 2),

            result="WIN" if pnl > 0 else "LOSS"

        )


        self.trades.append(trade)


        self.cash += pnl


        self.equity_curve.append(

            round(self.cash, 2)

        )


        return trade



    def run(
        self,
        symbol,
        dataframe,
        signals
    ):

        """
        Run full backtest.

        Uses next candle close as exit.
        """


        for signal in signals:


            index = signal["index"]


            if index + 1 >= len(dataframe):

                continue



            bias = signal["bias"]



            if bias == "BUY":

                direction = "LONG"


            elif bias == "SELL":

                direction = "SHORT"


            else:

                continue



            entry = float(

                dataframe["Close"].iloc[index]

            )


            exit_price = float(

                dataframe["Close"].iloc[index + 1]

            )



            self.execute(

                symbol,

                entry,

                direction,

                exit_price

            )



        return self.results()



    def equity(self):

        return round(

            self.cash,

            2

        )



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


        gross_loss = abs(

            sum(

                t.profit_loss

                for t in losses

            )

        )



        profit_factor = (

            round(

                gross_profit / gross_loss,

                2

            )

            if gross_loss > 0

            else "INF"

        )



        return {


            "starting_cash":

                self.starting_cash,


            "ending_equity":

                round(self.cash, 2),


            "net_profit":

                round(

                    self.cash - self.starting_cash,

                    2

                ),


            "return_percent":

                round(

                    (

                    (self.cash - self.starting_cash)

                    /

                    self.starting_cash

                    )

                    * 100,

                    2

                ),


            "total_trades":

                len(self.trades),


            "wins":

                len(wins),


            "losses":

                len(losses),


            "win_rate":

                round(

                    len(wins)

                    /

                    len(self.trades)

                    * 100,

                    2

                )

                if self.trades

                else 0,


            "profit_factor":

                profit_factor

        }