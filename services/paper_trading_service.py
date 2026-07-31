"""
Atlas AI Trading Platform 3.0

Paper Trading Service

Coordinates paper trading workflow.

Responsibilities:

- Select opportunities
- Validate positions
- Create trades
- Submit through broker
- Update portfolio
"""

from __future__ import annotations

from services.trade_service import TradeService



class PaperTradingService:


    def __init__(
        self,
        broker,
        position_manager,
        portfolio,
    ):

        self.broker = broker

        self.position_manager = position_manager

        self.portfolio = portfolio

        self.trade_service = TradeService()



    # ---------------------------------------------------------
    # Find best trade
    # ---------------------------------------------------------

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



    # ---------------------------------------------------------
    # Execute trade
    # ---------------------------------------------------------

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



        # Send order through broker

        trade = self.broker.submit_order(
            trade
        )



        self.portfolio.add_trade(
            trade
        )



        print(
            f"Paper trade opened: {trade.symbol}"
        )


        return trade