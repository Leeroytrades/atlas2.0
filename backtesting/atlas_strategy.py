"""
Atlas AI Trading Assistant 2.3

Atlas Backtesting Strategy Adapter

Connects historical market data
to the Atlas scoring engine.

Flow:

Historical Data
        ↓
Indicators
        ↓
Atlas Scorecard
        ↓
BUY / SELL / HOLD
"""


from __future__ import annotations


from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard



class AtlasStrategy:


    def __init__(

        self,

        confidence_threshold: int = 60

    ):

        self.confidence_threshold = confidence_threshold



    def analyse(

        self,

        dataframe

    ):

        """
        Analyse historical candle data.
        Returns:
        BUY
        SELL
        HOLD
        """


        if dataframe is None or dataframe.empty:

            return "HOLD"



        indicators = build_indicator_set(

            dataframe

        )


        scorecard = generate_scorecard(

            dataframe

        )


        score = scorecard.score



        confidence = scorecard.confidence



        if (

            score >= 60

            and confidence >= self.confidence_threshold

        ):

            return "BUY"



        if (

            score <= -60

            and confidence >= self.confidence_threshold

        ):

            return "SELL"



        return "HOLD"



    def signal(

        self,

        dataframe

    ):

        """
        Alias used by backtesting engine.
        """

        return self.analyse(

            dataframe

        )