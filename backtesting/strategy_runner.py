"""
Atlas Strategy Runner 3.0

Routes historical candles through the active strategy system.
"""

from __future__ import annotations

import pandas as pd

from strategies.router import StrategyRouter


class StrategyRunner:


    def __init__(
        self,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
    ):

        self.score_threshold = score_threshold
        self.confidence_threshold = confidence_threshold

        self.router = StrategyRouter()



    # -------------------------------------------------
    # Analyse candle
    # -------------------------------------------------

    def analyse(
        self,
        dataframe: pd.DataFrame,
        regime: str = "TREND",
    ):


        strategy = self.router.select(

            regime

        )


        if strategy is None:

            return None



        return strategy.generate_signal(

            dataframe

        )



    # -------------------------------------------------
    # Historical signal generation
    # -------------------------------------------------

    def run(
        self,
        dataframe: pd.DataFrame,
        symbol="UNKNOWN",
    ):


        results = []



        for index in range(

            50,

            len(dataframe)

        ):


            try:


                window = dataframe.iloc[

                    :index + 1

                ]



                # temporary regime detection
                # will later be replaced by ML regime engine

                close = window["Close"].iloc[-1]

                ema20 = window["EMA_20"].iloc[-1]

                ema50 = window["EMA_50"].iloc[-1]



                if (

                    ema20 > ema50
                    and close > ema20

                ):

                    regime = "BULLISH"



                elif (

                    ema20 < ema50
                    and close < ema20

                ):

                    regime = "BEARISH"



                else:

                    regime = "TREND"



                signal = self.analyse(

                    window,

                    regime,

                )


                if signal is None:

                    continue



                bias = signal["signal"]

                score = signal["score"]

                confidence = signal["confidence"]



                if bias not in (

                    "BUY",
                    "SELL"

                ):

                    continue



                if abs(score) < self.score_threshold:

                    continue



                if confidence < self.confidence_threshold:

                    continue



                results.append(

                    {

                        "index": index,

                        "date": dataframe.index[index],

                        "symbol": symbol,

                        "score": score,

                        "bias": bias,

                        "confidence": confidence,

                        "signal": bias,

                    }

                )


            except Exception as error:


                print(

                    f"Strategy error {index}: {error}"

                )

                continue



        return results