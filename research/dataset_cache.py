"""
Atlas AI Trading Platform 3.4

Research Dataset Cache

Creates and loads prepared research datasets.

Features:

- Extended historical datasets
- Indicator preparation
- Parquet caching
- Dataset validation
- Date range reporting
"""

from __future__ import annotations


from pathlib import Path

import pandas as pd


from data.market_data import MarketData

from indicators.composite import build_indicator_set



class DatasetCache:



    def __init__(
        self,
        directory: str = "data/cache",
    ):


        self.directory = Path(directory)


        self.directory.mkdir(

            parents=True,

            exist_ok=True,

        )


        self.market = MarketData()



    # =====================================================
    # Cache Path
    # =====================================================

    def get_path(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> Path:


        filename = (

            f"{symbol}_"

            f"{period}_"

            f"{interval}.parquet"

        )


        return self.directory / filename



    # =====================================================
    # Dataset Information
    # =====================================================

    def report(
        self,
        df: pd.DataFrame,
        symbol: str,
    ):


        print()

        print(
            "Dataset Information"
        )

        print(
            "-------------------"
        )


        print(
            f"Symbol: {symbol}"
        )


        print(
            f"Rows: {len(df)}"
        )


        if len(df):

            print(
                f"Start: {df.index.min()}"
            )

            print(
                f"End:   {df.index.max()}"
            )


        print()



    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        df: pd.DataFrame,
    ):


        minimum_rows = 1000


        if len(df) < minimum_rows:


            print()

            print(
                "WARNING:"
            )

            print(
                f"Dataset only contains {len(df)} rows."
            )

            print(
                f"Recommended minimum: {minimum_rows}"
            )

            print()



        return df



    # =====================================================
    # Load Dataset
    # =====================================================

    def load(
        self,
        symbol: str,
        period: str = "10y",
        interval: str = "1d",
        refresh: bool = False,
    ) -> pd.DataFrame:



        path = self.get_path(

            symbol,

            period,

            interval,

        )



        # ---------------------------------
        # Existing cache
        # ---------------------------------

        if path.exists() and not refresh:


            print()

            print(
                f"Loading cached dataset: {symbol}"
            )


            df = pd.read_parquet(

                path

            )


            self.report(

                df,

                symbol

            )


            return self.validate(

                df

            )



        # ---------------------------------
        # Build new dataset
        # ---------------------------------

        print()

        print(
            f"Building dataset: {symbol}"
        )

        print(
            f"Period: {period}"
        )

        print(
            f"Interval: {interval}"
        )



        df = self.market.get_history(

            symbol,

            period,

            interval,

        )



        if df.empty:


            raise ValueError(

                f"No market data returned for {symbol}"

            )



        print(
            "Building indicators..."
        )


        df = build_indicator_set(

            df

        )



        df.to_parquet(

            path

        )



        print()

        print(
            f"Saved cache: {path}"
        )



        self.report(

            df,

            symbol

        )


        return self.validate(

            df

        )



    # =====================================================
    # Clear Cache
    # =====================================================

    def clear(
        self,
        symbol: str | None = None,
    ):


        if symbol:


            for file in self.directory.glob(

                f"{symbol}_*.parquet"

            ):


                file.unlink()



        else:


            for file in self.directory.glob(

                "*.parquet"

            ):


                file.unlink()