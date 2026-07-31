"""
Atlas AI Trading Platform 3.0

Backtesting Strategy Runner

Configurable Atlas signal engine.

Applies:

- Score threshold filtering
- Confidence filtering
- Historical signal generation
"""

from __future__ import annotations


from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard





class StrategyRunner:


    def __init__(
        self,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
    ):

        self.score_threshold = score_threshold

        self.confidence_threshold = confidence_threshold





    def analyse(
        self,
        dataframe,
    ):


        indicators = build_indicator_set(

            dataframe

        )


        scorecard = generate_scorecard(

            indicators

        )


        return scorecard





    def run(
        self,
        dataframe,
        symbol="UNKNOWN",
    ):


        results = []



        for index in range(

            50,

            len(dataframe)

        ):



            window = dataframe.iloc[

                :index + 1

            ].copy()



            try:


                scorecard = self.analyse(

                    window

                )



                score = scorecard.total_score

                confidence = scorecard.confidence



                bias = scorecard.bias



                # ---------------------------------
                # Apply optimisation parameters
                # ---------------------------------

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