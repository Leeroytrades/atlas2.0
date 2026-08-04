"""
Atlas AI Trading Platform 3.5

Historical Data Loader

Provides extended market data
for backtesting and walk-forward validation.
"""

from __future__ import annotations


import pandas as pd


from data.market_data import MarketData





class HistoricalData:



    def __init__(self):

        self.market = MarketData()





    # =====================================================
    # LOAD HISTORICAL DATA
    # =====================================================

    def load(

        self,

        symbol: str,

        period: str = "10y",

        interval: str = "1d",

    ) -> pd.DataFrame:


        """
        Load extended historical candles.

        Designed for:

        - Backtesting
        - Optimisation
        - Walk-forward validation

        """



        print()

        print(

            f"Loading historical data: {symbol}"

        )

        print(

            f"Period: {period} | Interval: {interval}"

        )



        data = self.market.get_history(

            symbol,

            period=period,

            interval=interval,

        )



        if data is None or data.empty:


            raise ValueError(

                f"No historical data found for {symbol}"

            )



        data = data.copy()



        data = data.dropna()



        print(

            f"Loaded candles: {len(data)}"

        )



        return data