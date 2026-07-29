"""
Atlas AI Trading Assistant 2.1

Core Engine

Controls:
- Database
- Session
- Scanner
- Portfolio
- Risk
- Performance
- Equity tracking
- Trade monitoring
"""

from __future__ import annotations


from database.database import Database
from database.trades import TradeRepository
from database.equity_history import EquityHistoryRepository
from database.journal import JournalRepository

from services.performance_service import PerformanceService

from atlas.session import Session
from atlas.scanner import Scanner

from risk.position_manager import PositionManager
from risk.trade_monitor import TradeMonitor
from risk.risk_manager import create_trade

from performance.metrics import PerformanceMetrics


class AtlasEngine:


    def __init__(self):

        # Database

        self.database = Database()


        # Session

        self.session = Session()


        # Scanner

        self.scanner = Scanner()


        # Repositories

        self.trade_repository = TradeRepository(
            self.database
        )


        self.equity_history_repository = EquityHistoryRepository(
            self.database
        )


        self.journal = JournalRepository(
            self.database
        )


        # Risk

        self.position_manager = PositionManager(
            self.trade_repository
        )


        # Monitoring

        self.trade_monitor = TradeMonitor(
            self.trade_repository,
            self.journal
        )


        # Performance

        self.metrics = PerformanceMetrics(
            self.trade_repository
        )


        self.performance_service = PerformanceService(
            self.trade_repository
        )


        # Restore existing positions

        self.load_portfolio()



    # ---------------------------------
    # Market Scanner
    # ---------------------------------

    def scan_market(self):

        return self.scanner.scan(
            self.session.watchlist.symbols
        )



    # ---------------------------------
    # Analyse / Create Trade
    # ---------------------------------

    def analyse(
        self,
        symbol: str
    ):


        results = self.scan_market()


        score = next(

            (
                item
                for item in results
                if item.symbol == symbol
            ),

            None

        )


        if score is None:

            return None, None



        if score.bias != "BUY":

            return score, None



        if not self.position_manager.can_open_position(symbol):

            print(
                f"Existing position detected for {symbol}"
            )

            return score, None



        print(
            f"Trade opportunity found: {symbol}"
        )


        trade = create_trade(

            symbol=symbol,

            df=score.dataframe,

            account_balance=self.session.portfolio.account_balance,

            risk_percent=1.0,

            direction="LONG",

            confidence=score.confidence,

        )


        if trade is None:

            return score, None



        self.trade_repository.save(
            trade
        )


        self.session.portfolio.add_trade(
            trade
        )


        return score, trade



    # ---------------------------------
    # Portfolio
    # ---------------------------------

    def portfolio(self):

        return self.session.portfolio



    def load_portfolio(self):

        trades = self.trade_repository.open_trades()


        for trade in trades:

            self.session.portfolio.add_trade(
                trade
            )



    # ---------------------------------
    # Performance
    # ---------------------------------

    def performance(self):

        metrics = self.performance_service.summary()


        equity = metrics.get(

            "equity",

            self.session.portfolio.account_balance

        )


        self.equity_history_repository.save(
            equity
        )


        return metrics



    # ---------------------------------
    # Equity History
    # ---------------------------------

    def equity_history(self):

        return self.equity_history_repository.all()



    # ---------------------------------
    # Trade Monitoring
    # ---------------------------------

    def monitor_trades(self):

        trades = self.trade_repository.open_trades()


        results = []


        for trade in trades:


            try:

                current_price = self.scanner.market.get_history(
                    trade.symbol
                )["Close"].iloc[-1]


            except Exception:

                current_price = trade.entry



            state = self.trade_monitor.check_trade(

                trade,

                current_price

            )


            results.append(

                {

                    "symbol": trade.symbol,

                    "state": state.value,

                    "price": current_price

                }

            )


        return results



    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def close(self):

        self.database.close()