"""
Atlas AI Trading Platform 3.0

Optimisation Worker

Executes a single strategy configuration.

Designed for:

- Multiprocessing
- Parallel optimisation
- Distributed research
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
):
    """
    Run one optimisation configuration.

    Returns:
        dict containing:
        - parameters
        - backtest results
    """


    engine = BacktestEngine(
        starting_cash
    )


    result = engine.run(
        dataset,
        score_threshold,
        confidence,
        atr_stop,
        atr_target,
    )


    return {

        "score_threshold": score_threshold,

        "confidence": confidence,

        "atr_stop": atr_stop,

        "atr_target": atr_target,

        **result,

    }