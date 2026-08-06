"""
Atlas AI Trading Platform 4.0

Adaptive Strategy Runner

Single candle decision engine.

Used by:

- Backtesting
- Optimisation
- Validation
- Research

Returns ONE signal for the current window.
"""

from __future__ import annotations


import pandas as pd


from strategy.router import StrategyRouter
from research.regime_detector import RegimeDetector



class StrategyRunner:


    def __init__(
        self,
        score_threshold: int = 40,
        confidence_threshold: float = 0.40,
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

        strategy=None,

    ):


        if dataframe is None or len(dataframe) < 50:

            return None



        # -------------------------------------------------
        # Select strategy if not supplied
        # -------------------------------------------------

        if strategy is None:


            regime = self.regime_detector.analyse(

                dataframe

            )


            strategy = self.router.select(

                regime.get(

                    "regime",

                    "TREND"

                )

            )



        if strategy is None:

            return None



        # -------------------------------------------------
        # Generate strategy signal
        # -------------------------------------------------

        if hasattr(strategy, "generate_signal"):

            signal = strategy.generate_signal(

                dataframe

            )


        elif hasattr(strategy, "generate"):

            signal = strategy.generate(

                dataframe

            )


        else:

            return None



        if signal is None:

            return None



        # -------------------------------------------------
        # Normalise object/dict
        # -------------------------------------------------

        if not isinstance(signal, dict):


            signal = {


                "signal":

                    getattr(

                        signal,

                        "signal",

                        None

                    ),


                "score":

                    getattr(

                        signal,

                        "score",

                        0

                    ),


                "confidence":

                    getattr(

                        signal,

                        "confidence",

                        0

                    ),

            }



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

            return None



        if abs(score) < self.score_threshold:

            return None



        if confidence < self.confidence_threshold:

            return None



        return {


            "signal": bias,


            "bias": bias,


            "score": score,


            "confidence": confidence,


            "strategy":

                signal.get(

                    "strategy",

                    strategy.__class__.__name__

                ),


        }



    # =====================================================
    # BACKWARDS COMPATIBILITY
    # =====================================================

    def run(

        self,

        dataframe: pd.DataFrame,

        strategy=None,

    ):


        return self.analyse(

            dataframe,

            strategy,

        )