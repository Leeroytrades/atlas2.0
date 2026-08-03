"""
Atlas AI Trading Platform 3.3

Trend Strategy

Optimised trend-following strategy.

Features:

- Multi-timeframe trend confirmation
- EMA structure filter
- ADX strength filter
- MACD momentum confirmation
- RSI positioning
- Volatility validation
"""

from __future__ import annotations


import pandas as pd


from models.scorecard import Scorecard


from strategies.base import BaseStrategy


from scoring.trend_score import calculate_trend_score
from scoring.momentum_score import calculate_momentum_score
from scoring.volatility_score import calculate_volatility_score
from scoring.volume_score import calculate_volume_score



class TrendStrategy(BaseStrategy):


    name = "TREND"


    supported_regimes = [

        "TREND",

        "BULLISH",

        "BEARISH",

    ]


    # Compatibility with router/regime filter

    regimes = supported_regimes



    def __init__(

        self,

        buy_threshold: int = 40,

    ):


        super().__init__()


        self.buy_threshold = buy_threshold



    # =====================================================
    # Strategy Information
    # =====================================================

    def info(self):


        return {

            "name": self.name,

            "regimes": self.regimes,

            "enabled": True,

        }



    # =====================================================
    # Analysis
    # =====================================================

    def analyse(

        self,

        dataframe: pd.DataFrame,

    ) -> dict:


        scorecard = self.generate_scorecard(dataframe)


        return {

            "strategy": self.name,

            "signal": scorecard.signal,

            "score": scorecard.total_score,

            "confidence": scorecard.confidence,

        }



    # =====================================================
    # Signal
    # =====================================================

    def generate_signal(

        self,

        dataframe: pd.DataFrame,

    ) -> dict:


        scorecard = self.generate_scorecard(dataframe)


        return {

            "signal": scorecard.signal,

            "confidence": scorecard.confidence,

            "score": scorecard.total_score,

            "strategy": self.name,

        }



    # =====================================================
    # Core Logic
    # =====================================================

    def generate_scorecard(

        self,

        df: pd.DataFrame,

    ) -> Scorecard:



        row = df.iloc[-1]



        trend = calculate_trend_score(df)

        momentum = calculate_momentum_score(df)

        volatility = calculate_volatility_score(df)

        volume = calculate_volume_score(df)



        score = Scorecard()



        score.trend = trend.score

        score.momentum = momentum.score

        score.volatility = volatility.score

        score.volume = volume.score



        score.total_score = (

            score.trend

            +

            score.momentum

            +

            score.volatility

            +

            score.volume

        )



        close = float(row.get("Close", 0))

        ema20 = float(row.get("EMA_20", close))

        ema50 = float(row.get("EMA_50", close))

        ema200 = float(row.get("EMA_200", close))


        adx = float(row.get("ADX", 0))

        di_plus = float(row.get("DI_PLUS", 0))

        di_minus = float(row.get("DI_MINUS", 0))


        rsi = float(row.get("RSI", 50))

        macd_hist = float(row.get("MACD_HIST", 0))



        # =================================================
        # Filters
        # =================================================


        bullish_structure = (

            ema20 > ema50

        )


        bearish_structure = (

            ema20 < ema50

        )


        trend_strength = (

            adx >= 20

        )


        bullish_direction = (

            di_plus >= di_minus

        )


        bearish_direction = (

            di_minus > di_plus

        )


        momentum_confirmation = (

            45 < rsi < 75

            and

            macd_hist >= 0

        )


        volatility_confirmation = (

            volatility.score >= 0

        )


        volume_confirmation = (

            volume.score >= 0

        )


        pullback_confirmation = (

            close <= ema20 * 1.05

        )



        # =================================================
        # BUY
        # =================================================


        if (

            score.total_score >= self.buy_threshold

            and bullish_structure

            and trend_strength

            and bullish_direction

            and momentum_confirmation

            and volatility_confirmation

            and volume_confirmation

            and pullback_confirmation

        ):


            score.bullish = True

            score.signal = "BUY"



        # =================================================
        # SELL
        # =================================================


        elif (

            score.total_score <= -self.buy_threshold

            and bearish_structure

            and trend_strength

            and bearish_direction

        ):


            score.bearish = True

            score.signal = "SELL"



        else:


            score.signal = "HOLD"



        score.confidence = min(

            abs(score.total_score) / 100,

            1.0

        )


        return score



    # =====================================================
    # Explanation
    # =====================================================

    def explain(

        self,

        dataframe: pd.DataFrame,

    ) -> list[str]:


        reasons = []


        reasons.extend(

            calculate_trend_score(dataframe).reasons

        )


        reasons.extend(

            calculate_momentum_score(dataframe).reasons

        )


        reasons.extend(

            calculate_volatility_score(dataframe).reasons

        )


        reasons.extend(

            calculate_volume_score(dataframe).reasons

        )


        return reasons