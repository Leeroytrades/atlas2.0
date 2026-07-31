"""
Atlas AI Trading Platform 3.0

Multi Market Backtesting Engine

Runs Atlas backtests across multiple symbols.
"""

from __future__ import annotations


from backtesting.engine import BacktestEngine





class MultiBacktestEngine:


    def __init__(
        self,
        starting_cash: float = 100000.0,
    ):

        self.starting_cash = starting_cash



    # ==================================================
    # RUN MULTIPLE MARKETS
    # ==================================================

    def run(
        self,
        symbols: list[str],
    ):


        results = {}



        for symbol in symbols:


            print()

            print(
                f"Running backtest: {symbol}"
            )



            engine = BacktestEngine(

                self.starting_cash

            )


            try:

                result = engine.run(

                    symbol

                )


                results[symbol] = result



            except Exception as error:


                print(

                    f"Failed {symbol}: {error}"

                )



        return results