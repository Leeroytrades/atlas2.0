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


        # Database

        self.database = Database()



        # Journal

        self.journal = JournalRepository(

            self.database

        )



        # Core session

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



        # Risk

        self.position_manager = PositionManager(

            self.trade_repository

        )



        # Performance

        self.metrics = PerformanceMetrics(

            self.trade_repository

        )


        self.performance_service = PerformanceService(

            self.trade_repository

        )



        # Restore positions

        self.load_portfolio()



        # Journal engine start

        self.database.execute(

            """
            INSERT INTO journal
            (
                event,
                details,
                timestamp
            )

            VALUES (?,?,?)

            """,

            (
                "ENGINE_START",
                "Atlas Engine initialized",
                __import__("datetime")
                .datetime.now()
                .isoformat()
            )

        )



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



        self.journal.record_signal(

            symbol=symbol,

            direction=score.bias,

            entry=0,

            score=score.score,

            confidence=score.confidence,

            trend=getattr(score, "trend", 0),

            momentum=getattr(score, "momentum", 0),

            volatility=getattr(score, "volatility", 0),

            volume=getattr(score, "volume", 0),

            market_condition="SCANNED"

        )



        if score.bias == "BUY":


            if self.position_manager.can_open_position(symbol):


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


        monitored = []


        for trade in trades:


            monitored.append(

                trade

            )


        return monitored



    # ---------------------------------
    # Journal
    # ---------------------------------

    def journal_history(self):

        return self.journal.history()



    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def close(self):

        self.database.close()