"""
Atlas AI Trading Assistant 2.3

Historical Data Loader

Provides market data for backtesting.
"""

from __future__ import annotations

import pandas as pd

from data.market_data import MarketData


class HistoricalData:


    def __init__(self):

        self.market = MarketData()



    def load(
        self,
        symbol: str,
        period: str = "2y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Load historical candles.
        """

        data = self.market.get_history(
            symbol
        )


        if data is None or data.empty:

            raise ValueError(
                f"No historical data found for {symbol}"
            )


        return data.copy()