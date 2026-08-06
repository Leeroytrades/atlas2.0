"""
Atlas AI Trading Platform 4.0

Backtesting Engine

Research pipeline:

Historical Data
        |
Indicators
        |
Regime Detection
        |
Strategy Router
        |
Signal Validation
        |
Risk Sizing
        |
Trade Object
        |
Simulator
        |
Performance Metrics
"""

from __future__ import annotations


from typing import Dict, Any

import pandas as pd


from data.market_data import MarketData

from indicators.composite import build_indicator_set

from strategy.router import StrategyRouter

from strategy.regime_filter import RegimeFilter

from backtesting.simulator import Simulator

from models.trade import Trade



class BacktestEngine:


    def __init__(

        self,

        starting_cash: float = 100000.0,

        risk_percent: float = 1.0,

        minimum_score: int = 60,

        minimum_confidence: float = 0.60,

        atr_stop: float = 2.0,

        atr_target: float = 4.0,

        use_regime_filter: bool = True,

    ):


        self.starting_cash = starting_cash

        self.risk_percent = risk_percent

        self.minimum_score = minimum_score

        self.minimum_confidence = minimum_confidence

        self.atr_stop = atr_stop

        self.atr_target = atr_target

        self.use_regime_filter = use_regime_filter



        self.market = MarketData()


        self.router = StrategyRouter()



        self.regime_filter = RegimeFilter(

            allow_ranges=False,

            allow_high_volatility=True,

        )



        self.simulator = Simulator(

            starting_cash=starting_cash,

            atr_stop=atr_stop,

            atr_target=atr_target,

        )



    # =====================================================
    # RESET STATE
    # =====================================================

    def reset(self):

        """
        Reset simulator between optimisation runs.
        """

        self.simulator = Simulator(

            starting_cash=self.starting_cash,

            atr_stop=self.atr_stop,

            atr_target=self.atr_target,

        )



    # =====================================================
    # POSITION SIZE
    # =====================================================

    def position_size(

        self,

        entry: float,

        stop: float,

    ):


        risk_money = (

            self.starting_cash

            *

            self.risk_percent

            /

            100

        )


        distance = abs(

            entry - stop

        )


        if distance <= 0:

            return 1



        return max(

            int(

                risk_money /

                distance

            ),

            1

        )



    # =====================================================
    # RUN BACKTEST
    # =====================================================

    def run(

        self,

        symbol: str = "SPY",

        dataframe: pd.DataFrame | None = None,

        score_threshold: int | None = None,

        confidence_threshold: float | None = None,

        minimum_score: int | None = None,

        minimum_confidence: float | None = None,

        atr_stop: float | None = None,

        atr_target: float | None = None,

    ) -> Dict[str, Any]:


        self.reset()



        if atr_stop is not None:

            self.atr_stop = atr_stop



        if atr_target is not None:

            self.atr_target = atr_target



        if score_threshold is not None:

            self.minimum_score = score_threshold



        if minimum_score is not None:

            self.minimum_score = minimum_score



        if confidence_threshold is not None:

            self.minimum_confidence = confidence_threshold



        if minimum_confidence is not None:

            self.minimum_confidence = minimum_confidence



        # Only load market data if none supplied

        if dataframe is None:


            print()

            print(
                f"Loading historical data: {symbol}"
            )


            dataframe = self.market.get_history(

                symbol=symbol,

                period="10y",

                interval="1d",

            )


            if dataframe is None or dataframe.empty:

                return {

                    "trade_list": [],

                    "strategy_stats": {},

                    "net_profit": 0,

                }


            print(

                f"Loaded candles: {len(dataframe)}"

            )



        dataframe = build_indicator_set(

            dataframe.copy()

        )



        trades = []

        strategy_stats = {}



        index = 50



        while index < len(dataframe):


            window = dataframe.iloc[

                :index + 1

            ]



            if self.use_regime_filter:


                regime = self.regime_filter.evaluate(

                    window

                )


                if not regime["allowed"]:

                    index += 1

                    continue


                strategy = self.router.select(

                    regime["regime"]

                )


            else:


                strategy = self.router.select(

                    "TREND"

                )



            if strategy is None:

                index += 1

                continue



            strategy_name = (

                strategy.__class__.__name__

            )



            if strategy_name not in strategy_stats:


                strategy_stats[strategy_name] = {

                    "trades": 0,

                    "wins": 0,

                    "losses": 0,

                }



            signal = strategy.generate_signal(

                window

            )



            if signal is None:

                index += 1

                continue



            score = signal.get(

                "score",

                0

            )


            confidence = signal.get(

                "confidence",

                0

            )



            if score < self.minimum_score:

                index += 1

                continue



            if confidence < self.minimum_confidence:

                index += 1

                continue



            candle = dataframe.iloc[index]



            entry = float(

                candle["Close"]

            )


            atr = float(

                candle["ATR"]

            )



            if signal.get("signal") == "BUY":


                direction = "LONG"


                stop = entry - (

                    atr * self.atr_stop

                )


                target = entry + (

                    atr * self.atr_target

                )


            else:


                direction = "SHORT"


                stop = entry + (

                    atr * self.atr_stop

                )


                target = entry - (

                    atr * self.atr_target

                )



            quantity = self.position_size(

                entry,

                stop,

            )



            trade = Trade(

                symbol=symbol,

                direction=direction,

                entry=entry,

                stop_loss=stop,

                take_profit=target,

                quantity=quantity,

                confidence=confidence,

                notes=strategy_name,

            )



            simulated = self.simulator.simulate_trade(

                trade,

                dataframe,

                index,

            )


            simulated.strategy = strategy_name



            trades.append(

                simulated

            )



            strategy_stats[strategy_name]["trades"] += 1



            if simulated.profit_loss > 0:

                strategy_stats[strategy_name]["wins"] += 1

            else:

                strategy_stats[strategy_name]["losses"] += 1



            index = max(

                index + 1,

                simulated.exit_index + 1

            )



        net_profit = sum(

            t.profit_loss

            for t in trades

        )



        return {


            "symbol":

                symbol,


            "trade_list":

                trades,


            "strategy_stats":

                strategy_stats,


            "net_profit":

                round(

                    net_profit,

                    2

                ),


            "ending_equity":

                round(

                    self.simulator.cash,

                    2

                ),


            "equity_curve":

                self.simulator.equity_curve,


            "max_drawdown":

                self.simulator.calculate_drawdown(),


            "simulator_results":

                self.simulator.results(),


            "regime_stats":

                self.regime_filter.statistics(),

        }