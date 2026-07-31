"""
Atlas AI Trading Assistant 3.0

Application Engine

Coordinates:

- Session
- Scanner Service
- Paper Trading
- Execution
- Performance
- Portfolio
- Database
"""

from __future__ import annotations


from database.database import Database
from database.trades import TradeRepository
from database.equity_history import EquityHistoryRepository
from database.journal import JournalRepository


from data.market_data import MarketData


from atlas.session import Session
from atlas.scanner import Scanner


from execution.manager import ExecutionManager


from risk.position_manager import PositionManager


from services.scanner_service import ScannerService
from services.paper_trading_service import PaperTradingService
from services.execution_service import ExecutionService
from services.performance_service import PerformanceService
from services.portfolio_service import PortfolioService



class AtlasEngine:
    """
    Main application coordinator.
    """


    def __init__(self):


        # ==============================
        # DATABASE
        # ==============================

        self.database = Database()


        self.trades = TradeRepository(
            self.database
        )


        self.equity_history_repository = EquityHistoryRepository(
            self.database
        )


        self.journal = JournalRepository(
            self.database
        )


        # ==============================
        # SESSION
        # ==============================

        self.session = Session()



        # ==============================
        # MARKET
        # ==============================

        self.market = MarketData()



        # ==============================
        # CORE COMPONENTS
        # ==============================

        self.scanner = Scanner()


        self.position_manager = PositionManager(
            self.trades
        )


        self.execution_manager = ExecutionManager(
            self.trades
        )



        # ==============================
        # SERVICES
        # ==============================

        self.scanner_service = ScannerService(

            self.session,

            self.scanner,

        )


        self.paper_trading = PaperTradingService(

            self.trades,

            self.position_manager,

            self.session.portfolio,

        )


        self.execution_service = ExecutionService(

            self.execution_manager,

            self.trades,

            self.market,

        )


        self.performance_service = PerformanceService(

            self.trades,

        )


        self.portfolio_service = PortfolioService(

            self.session.portfolio,

            self.trades,

        )


        self.load_portfolio()



    # ==================================================
    # SCANNING
    # ==================================================

    def scan_market(self):

        return self.scanner_service.scan()



    # ==================================================
    # PAPER TRADING
    # ==================================================

    def search_and_trade(
        self,
        scans,
    ):

        return self.paper_trading.trade_best(
            scans
        )



    # ==================================================
    # EXECUTION / MONITORING
    # ==================================================

    def monitor_trades(self):

        return self.execution_service.monitor()



    # ==================================================
    # PORTFOLIO
    # ==================================================

    def portfolio(self):

        return self.session.portfolio



    def load_portfolio(self):

        trades = self.trades.open_trades()


        for trade in trades:

            self.session.portfolio.add_trade(
                trade
            )



    # ==================================================
    # PERFORMANCE
    # ==================================================

    def performance(self):

        metrics = self.performance_service.summary()


        equity = metrics.get(

            "equity",

            self.session.portfolio.account_balance,

        )


        latest = self.equity_history_repository.latest()


        if latest is None or latest["equity"] != equity:

            self.equity_history_repository.save(
                equity
            )


        return metrics



    # ==================================================
    # EQUITY HISTORY
    # ==================================================

    def equity_history(self):

        return self.equity_history_repository.all()



    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.database.close()