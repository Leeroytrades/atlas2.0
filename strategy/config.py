"""
Atlas AI Trading Platform 3.8

Strategy Configuration

Centralises:
- score thresholds
- confidence requirements
- regime filters
- quality controls

"""

from __future__ import annotations



class StrategyConfig:


    # =====================================================
    # Strategy thresholds
    # =====================================================

    SCORE_THRESHOLDS = {


        "TrendStrategy":

            50,


        "RangeStrategy":

            45,


        "VolatilityStrategy":

            60,


    }



    CONFIDENCE_THRESHOLDS = {


        "TrendStrategy":

            0.55,


        "RangeStrategy":

            0.60,


        "VolatilityStrategy":

            0.65,


    }



    # =====================================================
    # Regime confidence
    # =====================================================

    MIN_REGIME_CONFIDENCE = 0.70



    # =====================================================
    # Signal quality
    # =====================================================

    MIN_SCORE_DISTANCE = 10



    # =====================================================
    # Trade controls
    # =====================================================

    MIN_CANDLES_BETWEEN_TRADES = 20



    @classmethod
    def score_threshold(cls, strategy):


        return cls.SCORE_THRESHOLDS.get(

            strategy,

            50

        )



    @classmethod
    def confidence_threshold(cls, strategy):


        return cls.CONFIDENCE_THRESHOLDS.get(

            strategy,

            0.5

        )