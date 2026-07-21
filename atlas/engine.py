"""
Atlas AI Trading Assistant 2.0

Core Engine

Controls:
- Database
- Session
- Scanner
- Portfolio
- Risk
- Performance
- Equity tracking
- Trade Journal
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

from performance.metrics import PerformanceMetrics



class AtlasEngine:


    def __init__(self):


        # -----------------------------
        # Database
        # -----------------------------

        self.database = Database()



        # -----------------------------
        # Core Session
        # -----------------------------

        self.session = Session()



        # -----------------------------
        # Market Scanner
        # -----------------------------

        self.scanner = Scanner()



        # -----------------------------
        # Repositories
        # -----------------------------

        self.trade_repository = TradeRepository(

            self.database

        )


        self.equity_history_repository = EquityHistoryRepository(

            self.database

        )


        self.journal_repository = JournalRepository(

            self.database

        )



        # -----------------------------
        # Risk / Positions
        # -----------------------------

        self.position_manager = PositionManager(

            self.trade_repository

        )



        # -----------------------------
        # Performance
        # -----------------------------

        self.metrics = PerformanceMetrics(

            self.trade_repository

        )


        self.performance_service = PerformanceService(

            self.trade_repository

        )



        # -----------------------------
        # Restore Portfolio
        # -----------------------------

        self.load_portfolio()



    # ---------------------------------
    # Market Scanner
    # ---------------------------------

    def scan_market(self):


        return self.scanner.scan(

            self.session.watchlist.symbols

        )



    # ---------------------------------
    # Analyse Symbol
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



        trade = None



        if score.bias == "BUY":



            if self.position_manager.can_open_position(

                symbol

            ):


                print(

                    f"Trade opportunity found: {symbol}"

                )



            else:


                print(

                    f"Existing position detected for {symbol}"

                )

                print(

                    "Trade creation skipped."

                )



        return score, trade



    # ---------------------------------
    # Record Journal Entry
    # ---------------------------------

    def record_signal(

        self,

        symbol: str,

        direction: str,

        entry: float,

        score

    ):


        self.journal_repository.record_signal(

            symbol=symbol,

            direction=direction,

            entry=entry,

            score=score.score,

            confidence=score.confidence,

            trend=score.trend,

            momentum=score.momentum,

            volatility=score.volatility,

            volume=score.volume

        )



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
    # Trade Journal
    # ---------------------------------

    def journal(self):


        return self.journal_repository.history()



    # ---------------------------------
    # Trade Monitoring
    # ---------------------------------

    def monitor_trades(self):

        return None



    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def close(self):


        self.database.close()