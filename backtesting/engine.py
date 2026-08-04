"""
Atlas AI Trading Platform 3.6

Adaptive Backtesting Engine

Adds:

- Regime detection
- Strategy routing
- Trend strategy
- Range strategy
- Volatility fallback
- Dynamic parameters
"""

from __future__ import annotations


import pandas as pd


from backtesting.historical_data import HistoricalData
from backtesting.simulator import Simulator


from risk.risk_manager import create_trade


from indicators.composite import build_indicator_set


from research.regime_detector import RegimeDetector


from strategy.router import StrategyRouter



class BacktestEngine:


    _data_cache: dict[str, pd.DataFrame] = {}



    def __init__(

        self,

        starting_cash: float = 100000.0,

        use_regime_filter: bool = True,

    ):


        self.starting_cash = starting_cash

        self.use_regime_filter = use_regime_filter


        self.data_loader = HistoricalData()


        self.regime_detector = RegimeDetector()


        self.router = StrategyRouter()



    # =====================================================
    # LOAD DATA
    # =====================================================

    def _get_data(

        self,

        symbol,

    ):


        if symbol in self._data_cache:

            return self._data_cache[symbol]



        data = self.data_loader.load(

            symbol

        )


        data = build_indicator_set(

            data

        )


        self._data_cache[symbol] = data


        return data



    # =====================================================
    # RUN
    # =====================================================

    def run(

        self,

        symbol,

        score_threshold=40,

        confidence_threshold=0.4,

        atr_stop=4.0,

        atr_target=6.0,

    ):



        if isinstance(symbol,pd.DataFrame):


            dataframe = symbol.copy()

            trade_symbol="UNKNOWN"



            if "ATR" not in dataframe.columns:

                dataframe = build_indicator_set(

                    dataframe

                )


        else:


            trade_symbol=symbol


            dataframe=self._get_data(

                symbol

            )



        simulator = Simulator(

            starting_cash=self.starting_cash,

            atr_stop=atr_stop,

            atr_target=atr_target,

        )



        last_exit=-1



        for i in range(

            200,

            len(dataframe)

        ):



            window=dataframe.iloc[:i+1]



            regime = self.regime_detector.analyse(

                window

            )



            strategy = self.router.select(

                regime["regime"]

            )



            signal = strategy.generate_signal(

                window

            )



            if signal["signal"] not in (

                "BUY",

                "SELL"

            ):

                continue



            if abs(signal["score"]) < score_threshold:

                continue



            if signal["confidence"] < confidence_threshold:

                continue



            if i <= last_exit:

                continue



            direction = (

                "LONG"

                if signal["signal"]=="BUY"

                else

                "SHORT"

            )



            trade=create_trade(

                trade_symbol,

                window,

                self.starting_cash,

                1.0,

                direction,

                signal["confidence"],

            )



            if trade is None:

                continue



            result=simulator.simulate_trade(

                trade,

                dataframe,

                i,

            )



            if result:

                last_exit=result.exit_index



        return simulator.results()