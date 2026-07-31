"""
Atlas AI Trading Platform 3.0

Paper Trading Service

Coordinates paper trading workflow.
"""

from __future__ import annotations


from services.trade_service import TradeService



class PaperTradingService:


    def __init__(
        self,
        broker,
        position_manager,
        portfolio,
        alerts=None,
    ):

        self.broker = broker

        self.position_manager = position_manager

        self.portfolio = portfolio

        self.alerts = alerts

        self.trade_service = TradeService()



    def trade_best(
        self,
        scans,
    ):


        candidates = [

            scan

            for scan in scans

            if scan.bias == "BUY"

        ]



        if not candidates:

            return None



        candidates.sort(

            key=lambda x: x.confidence,

            reverse=True

        )



        for scan in candidates:


            trade = self.execute_scan(
                scan
            )


            if trade:

                return trade



        return None



    def execute_scan(
        self,
        scan,
    ):


        if self.position_manager.has_open_position(

            scan.symbol

        ):

            return None



        trade = self.trade_service.create(

            symbol=scan.symbol,

            df=scan.dataframe,

            score=scan,

            account_balance=self.portfolio.account_balance,

        )



        if trade is None:

            return None



        if not self.position_manager.can_open_position(

            scan.symbol,

            trade.risk_amount,

        ):

            return None



        trade = self.broker.submit_order(
            trade
        )



        self.portfolio.add_trade(
            trade
        )



        if self.alerts:

            self.alerts.trade_opened(
                trade
            )



        print(
            f"Paper trade opened: {trade.symbol}"
        )


        return trade