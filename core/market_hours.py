"""
Atlas AI Trading Platform

Market Hours Controller

Controls when Atlas is allowed
to scan and trade.
"""

from __future__ import annotations


from datetime import datetime, time


from core.config import Config





class MarketHours:


    def __init__(
        self,
    ):


        self.enabled = Config.MARKET_ENABLED



        self.open_time = time(

            Config.MARKET_OPEN_HOUR,

            Config.MARKET_OPEN_MINUTE

        )



        self.close_time = time(

            Config.MARKET_CLOSE_HOUR,

            Config.MARKET_CLOSE_MINUTE

        )



    # ==================================================
    # CHECK MARKET STATUS
    # ==================================================

    def is_open(
        self,
    ) -> bool:



        if not self.enabled:

            return True



        now = datetime.now().time()



        return (

            self.open_time

            <=

            now

            <=

            self.close_time

        )



    # ==================================================
    # STATUS
    # ==================================================

    def status(
        self,
    ) -> str:


        if self.is_open():

            return "OPEN"



        return "CLOSED"



    # ==================================================
    # SUMMARY
    # ==================================================

    def summary(
        self,
    ) -> dict:


        return {

            "enabled": self.enabled,

            "status": self.status(),

            "open": self.open_time.isoformat(),

            "close": self.close_time.isoformat(),

        }