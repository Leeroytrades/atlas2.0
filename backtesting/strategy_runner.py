"""
Atlas AI Trading Platform 3.2

Backtesting Strategy Runner

Optimised signal engine.

Improvements:

- Uses pre-calculated indicator datasets
- Avoids rebuilding indicators every candle
- Faster optimisation
- Same signal logic
"""

from __future__ import annotations

import pandas as pd

from strategy.signal_generator import generate_scorecard



class StrategyRunner:


    def __init__(
        self,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
    ):

        self.score_threshold = score_threshold

        self.confidence_threshold = confidence_threshold



    # ---------------------------------------------------------
    # Analyse existing indicator dataframe
    # ---------------------------------------------------------

    def analyse(
        self,
        dataframe: pd.DataFrame,
    ):


        scorecard = generate_scorecard(

            dataframe,

            buy_threshold=self.score_threshold

        )


        return scorecard



    # ---------------------------------------------------------
    # Generate historical signals
    # ---------------------------------------------------------

    def run(
        self,
        dataframe: pd.DataFrame,
        symbol="UNKNOWN",
    ):


        results = []



        # Indicators already exist.
        # No rebuilding on every candle.

        for index in range(

            50,

            len(dataframe)

        ):


            try:


                window = dataframe.iloc[

                    :index + 1

                ]



                scorecard = self.analyse(

                    window

                )



                score = scorecard.total_score

                confidence = scorecard.confidence

                bias = scorecard.bias



                if bias == "BUY":


                    if score < self.score_threshold:

                        continue



                    if confidence < self.confidence_threshold:

                        continue



                elif bias == "SELL":


                    if abs(score) < self.score_threshold:

                        continue



                    if confidence < self.confidence_threshold:

                        continue



                else:

                    continue



                results.append(

                    {

                        "index": index,

                        "date": dataframe.index[index],

                        "symbol": symbol,

                        "score": score,

                        "bias": bias,

                        "confidence": confidence,

                        "signal": scorecard.signal,

                        "scorecard": scorecard,

                    }

                )



            except Exception as error:


                print(

                    f"Backtest error {index}: {error}"

                )

                continue



        return results