"""
Atlas AI Trading Platform 3.6

Adaptive Strategy Runner

Routes historical candles through:

- Regime Detector
- Strategy Router
- Active Strategy

Used by:

Backtesting
Optimisation
Validation
Research
"""

from __future__ import annotations


import pandas as pd


from strategy.router import StrategyRouter

from research.regime_detector import RegimeDetector



class StrategyRunner:


    def __init__(
        self,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
    ):


        self.score_threshold = score_threshold

        self.confidence_threshold = confidence_threshold


        self.router = StrategyRouter()

        self.regime_detector = RegimeDetector()



    # =====================================================
    # ANALYSE CURRENT WINDOW
    # =====================================================

    def analyse(
        self,
        dataframe: pd.DataFrame,
    ):


        regime_data = self.regime_detector.analyse(

            dataframe

        )


        regime = "TREND"

        regime_confidence = 0



        if isinstance(
            regime_data,
            dict
        ):


            regime = regime_data.get(

                "regime",

                "TREND"

            )


            regime_confidence = regime_data.get(

                "confidence",

                0

            )


        else:

            regime = regime_data



        strategy = self.router.select(

            regime

        )



        if strategy is None:

            return None



        signal = strategy.generate_signal(

            dataframe

        )


        if signal is None:

            return None



        signal["regime"] = regime

        signal["regime_confidence"] = regime_confidence

        signal["selected_strategy"] = strategy.name



        return signal



    # =====================================================
    # HISTORICAL RUN
    # =====================================================

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



                signal = self.analyse(

                    window

                )



                if signal is None:

                    continue



                bias = signal.get(

                    "signal"

                )


                score = signal.get(

                    "score",

                    0

                )


                confidence = signal.get(

                    "confidence",

                    0

                )



                if bias not in (

                    "BUY",

                    "SELL",

                ):

                    continue



                if abs(score) < self.score_threshold:

                    continue



                if confidence < self.confidence_threshold:

                    continue



                results.append(

                    {

                        "index":

                            index,


                        "date":

                            dataframe.index[index],


                        "symbol":

                            symbol,


                        "score":

                            score,


                        "bias":

                            bias,


                        "confidence":

                            confidence,


                        "signal":

                            bias,


                        "regime":

                            signal.get(

                                "regime",

                                "UNKNOWN"

                            ),


                        "strategy":

                            signal.get(

                                "selected_strategy",

                                "UNKNOWN"

                            ),

                    }

                )



            except Exception as error:


                print(

                    f"Strategy error {index}: {error}"

                )


                continue



        return results