"""
Atlas AI Trading Assistant 3.0

Multi Market Backtesting Engine

Runs Atlas across multiple symbols
and combines performance results.
"""

from __future__ import annotations


from backtesting.engine import BacktestEngine



class MultiMarketBacktester:


    def __init__(
        self,
        symbols: list[str],
        starting_cash: float = 100000.0
    ):

        self.symbols = symbols

        self.starting_cash = starting_cash

        self.results = {}



    def run(self):

        """
        Run backtests across all symbols.
        """


        for symbol in self.symbols:


            print(
                f"\nRunning {symbol}..."
            )


            engine = BacktestEngine(

                starting_cash=self.starting_cash

            )


            result = engine.run(

                symbol

            )


            self.results[symbol] = result



        return self.results




    def summary(self):

        """
        Create combined summary.
        """


        total_profit = 0

        total_trades = 0

        total_wins = 0


        for result in self.results.values():


            total_profit += (

                result["net_profit"]

            )


            total_trades += (

                result["total_trades"]

            )


            total_wins += (

                result["wins"]

            )



        win_rate = (

            total_wins

            /

            total_trades

            *

            100

            if total_trades

            else 0

        )



        return {


            "markets_tested":

                len(self.results),


            "total_trades":

                total_trades,


            "wins":

                total_wins,


            "combined_profit":

                round(

                    total_profit,

                    2

                ),


            "combined_win_rate":

                round(

                    win_rate,

                    2

                )

        }