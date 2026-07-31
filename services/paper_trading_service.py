"""
Atlas AI Trading Assistant 3.0

Paper Trading Service

Coordinates the complete paper trading workflow.

Responsibilities

- Select opportunities
- Validate positions
- Create trades
- Save trades
- Update portfolio

This service intentionally contains orchestration only.

Trade creation belongs to TradeService.
Risk validation belongs to PositionManager.
Persistence belongs to TradeRepository.
"""

from __future__ import annotations

from services.trade_service import TradeService


class PaperTradingService:
    """
    Coordinates paper trade execution.
    """

    def __init__(
        self,
        trade_repository,
        position_manager,
        portfolio,
    ):

        self.trade_repository = trade_repository

        self.position_manager = position_manager

        self.portfolio = portfolio

        self.trade_service = TradeService()

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def trade_best(
        self,
        scans,
    ):
        """
        Execute the highest-confidence BUY opportunity.

        Returns:
            Trade | None
        """

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

            trade = self.execute_scan(scan)

            if trade:

                return trade

        return None

    # ---------------------------------------------------------
    # Execute Scan
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

        self.trade_repository.save(
            trade
        )

        self.portfolio.add_trade(
            trade
        )

        print(
            f"Paper trade opened: {trade.symbol}"
        )

        return trade