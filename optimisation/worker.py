"""
Atlas AI Trading Platform 3.3

Optimisation Worker

Runs one optimisation configuration.

Supports:

- Parameter testing
- Regime filter experiments
"""

from __future__ import annotations


from backtesting.engine import BacktestEngine



def run_configuration(

    dataset,

    symbol: str,

    starting_cash: float,

    score_threshold: int,

    confidence: float,

    atr_stop: float,

    atr_target: float,

    use_regime_filter: bool = False,

):


    engine = BacktestEngine(

        starting_cash=starting_cash,

        use_regime_filter=use_regime_filter,

    )


    results = engine.run(

        dataset,

        score_threshold=int(score_threshold),

        confidence_threshold=float(confidence),

        atr_stop=float(atr_stop),

        atr_target=float(atr_target),

    )


    return results