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


    def __init__(self):


        # -----------------------------
        # Database
        # -----------------------------

        self.database = Database()


        self.trades = TradeRepository(
            self.database
        )


        self.equity_history = EquityHistoryRepository(
            self.database
        )


        self.journal = JournalRepository(
            self.database
        )


        # -----------------------------
        # Session
        # -----------------------------

        self.session = Session()



        # -----------------------------
        # Core components
        # -----------------------------

        self.scanner = Scanner()


        self.position_manager = PositionManager(
            self.trades
        )


        self.execution_manager = ExecutionManager(
            self.trades
        )


        # -----------------------------
        # Services
        # -----------------------------

        self.scanner_service = ScannerService(

            self.session,

            self.scanner

        )


        self.paper_trading = PaperTradingService(

            self.trades,

            self.position_manager,

            self.session.portfolio,

        )


        self.execution_service = ExecutionService(

            self.execution_manager,

            self.trades,

            self.scanner.market,

        )


        self.performance_service = PerformanceService(

            self.trades

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
    # EXECUTION
    # ==================================================

    def monitor_trades(self):

        return self.execution_service.monitor()



    # ==================================================
    # PERFORMANCE
    # ==================================================

    def performance(self):

        return self.performance_service.summary()



    # ==================================================
    # PORTFOLIO
    # ==================================================

    def portfolio(self):

        return self.session.portfolio



    # ==================================================
    # EQUITY
    # ==================================================

    def equity_history_data(self):

        return self.equity_history.all()



    # ==================================================
    # LOAD EXISTING TRADES
    # ==================================================

    def load_portfolio(self):

        trades = self.trades.open_trades()


        for trade in trades:

            self.session.portfolio.add_trade(
                trade
            )



    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.database.close()