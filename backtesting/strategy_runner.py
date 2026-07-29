"""
Atlas AI Trading Assistant 2.3

Backtesting Strategy Runner

Runs Atlas scoring logic across historical data.
"""

from __future__ import annotations


from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard



class StrategyRunner:


    def __init__(self):

        pass



    def analyse(
        self,
        dataframe
    ):

        """
        Run Atlas strategy against candle data.
        """


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
        symbol="UNKNOWN"
    ):

        """
        Execute Atlas strategy through historical candles.

        Returns generated signals.
        """


        results = []


        for index in range(
            50,
            len(dataframe)
        ):


            window = dataframe.iloc[:index].copy()


            try:

                scorecard = self.analyse(
                    window
                )


                results.append(

                    {

                        "index": index,

                        "date": dataframe.index[index],

                        "symbol": symbol,

                        "score": scorecard.total_score,

                        "bias": scorecard.bias,

                        "confidence": scorecard.confidence,

                        "signal": scorecard.signal,

                        "scorecard": scorecard

                    }

                )


            except Exception as error:


                print(
                    f"Backtest error {index}: {error}"
                )

                continue



        return results