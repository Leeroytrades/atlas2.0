"""
Atlas AI Trading Platform 3.0

Paper Trading Service

Coordinates the trading workflow.

Responsibilities:

- Select opportunities
- Validate positions
- Create trades
- Submit trades through broker
- Update portfolio

Persistence and execution are handled by the broker layer.
"""

from __future__ import annotations


from services.trade_service import TradeService



class PaperTradingService:
    """
    Coordinates paper trade execution.
    """


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
    # Find and execute best opportunity
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

            reverse=True,

        )



        for scan in candidates:


            trade = self.execute_scan(
                scan
            )


            if trade:

                return trade



        return None



    # ---------------------------------------------------------
    # Execute Trade
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



        # -----------------------------
        # Send order through broker
        # -----------------------------

        executed_trade = self.broker.submit_order(
            trade
        )


        self.portfolio.add_trade(
            executed_trade
        )


        print(
            f"Paper trade opened: {executed_trade.symbol}"
        )


        return executed_trade