"""
Atlas AI Trading Platform

Broker Factory

Creates the active broker.
"""

from __future__ import annotations


from brokers.paper import PaperBroker



def create_broker(
    mode,
    trade_repository,
):

    mode = mode.upper()


    if mode == "PAPER":

        return PaperBroker(
            trade_repository
        )


    raise ValueError(
        f"Unsupported broker mode: {mode}"
    )