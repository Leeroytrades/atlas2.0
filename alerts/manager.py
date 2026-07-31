"""
Atlas AI Trading Platform

Alert Manager

Central alert dispatcher.
"""

from __future__ import annotations


from alerts.console import ConsoleAlert



class AlertManager:
    """
    Handles application alerts.
    """


    def __init__(
        self,
        alert=None,
    ):

        self.alert = alert or ConsoleAlert()



    def send(
        self,
        message: str,
    ) -> None:

        self.alert.send(
            message
        )



    def trade_opened(
        self,
        trade,
    ):

        self.send(

            f"Trade opened: "
            f"{trade.symbol} "
            f"{trade.direction} "
            f"Entry {trade.entry}"

        )



    def trade_closed(
        self,
        trade,
    ):

        self.send(

            f"Trade closed: "
            f"{trade.symbol} "
            f"P/L {trade.profit_loss}"

        )



    def signal_found(
        self,
        signal,
    ):

        self.send(

            f"Signal found: "
            f"{signal.symbol} "
            f"{signal.action}"

        )