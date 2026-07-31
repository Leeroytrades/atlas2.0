"""
Atlas AI Trading Platform 3.0

Application Engine

Coordinates:

- Session
- Scanner
- Paper Trading
- Broker
- Execution
- Performance
- Portfolio
- Database
- Backtesting
"""

from __future__ import annotations


from database.database import Database
from database.trades import TradeRepository
from database.equity_history import EquityHistoryRepository
from database.journal import JournalRepository


from data.market_data import MarketData


from atlas.session import Session
from atlas.scanner import Scanner


from brokers.factory import create_broker


from risk.position_manager import PositionManager


from services.scanner_service import ScannerService
from services.paper_trading_service import PaperTradingService
from services.execution_service import ExecutionService
from services.performance_service import PerformanceService
from services.portfolio_service import PortfolioService
from services.backtesting_service import BacktestingService



try:

    from core.config import BROKER_MODE

except ImportError:

    BROKER_MODE = "PAPER"





class AtlasEngine:


    def __init__(self):


        # ==================================================
        # DATABASE
        # ==================================================

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



        # ==================================================
        # SESSION
        # ==================================================

        self.session = Session()



        # ==================================================
        # MARKET
        # ==================================================

        self.market = MarketData()


        self.scanner = Scanner()



        # ==================================================
        # RISK
        # ==================================================

        self.position_manager = PositionManager(

            self.trades

        )



        # ==================================================
        # BROKER
        # ==================================================

        self.broker = create_broker(

            BROKER_MODE,

            self.trades,

        )



        # ==================================================
        # SERVICES
        # ==================================================

        self.scanner_service = ScannerService(

            self.session,

            self.scanner,

        )


        self.paper_trading = PaperTradingService(

            self.broker,

            self.position_manager,

            self.session.portfolio,

        )


        self.execution_service = ExecutionService(

            self.broker,

            self.trades,

            self.market,

        )


        self.performance_service = PerformanceService(

            self.trades

        )


        self.portfolio_service = PortfolioService(

            self.session.portfolio,

            self.trades,

        )


        self.backtesting_service = BacktestingService()



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
    # EXECUTION
    # ==================================================

    def monitor_trades(self):

        return self.execution_service.monitor()



    # ==================================================
    # PERFORMANCE
    # ==================================================

    def performance(self):

        metrics = self.performance_service.summary()


        equity = metrics.get(

            "equity",

            self.session.portfolio.account_balance

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
    # BACKTESTING
    # ==================================================

    def run_backtest(
        self,
        symbol: str,
    ):

        return self.backtesting_service.run(

            symbol

        )



    def rank_backtests(
        self,
        results: dict,
        count: int = 3,
    ):

        return self.backtesting_service.rank_markets(

            results,

            count

        )



    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.database.close()