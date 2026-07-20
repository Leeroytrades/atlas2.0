"""
Atlas AI Trading Assistant 2.0

Main Engine
"""

from __future__ import annotations


from atlas.session import Session

from atlas.scanner import Scanner

from data.market_data import MarketData

from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard

from risk.risk_manager import create_trade

from risk.position_manager import PositionManager


from database.database import Database

from database.trades import TradeRepository

from database.portfolio import PortfolioRepository

from database.journal import JournalRepository


from execution.manager import ExecutionManager


from performance.metrics import PerformanceMetrics



class AtlasEngine:


    def __init__(self):

        self.session = Session()

        self.market = MarketData()

        self.scanner = Scanner()


        self.database = Database()


        self.trades = TradeRepository(
            self.database
        )


        self.positions = PositionManager(
            self.trades
        )


        self.performance_tracker = PerformanceMetrics(
            self.trades
        )


        self.portfolio_repository = PortfolioRepository(
            self.database
        )


        self.journal = JournalRepository(
            self.database
        )


        self.execution = ExecutionManager(
            self.trades
        )



    def scan_market(self):

        return self.scanner.scan(
            self.session.watchlist.all()
        )



    def analyse(
        self,
        symbol: str
    ):

        if not self.positions.can_open_position(
            symbol
        ):

            return None, None



        df = self.market.get_history(
            symbol
        )


        df = build_indicator_set(
            df
        )


        score = generate_scorecard(
            df
        )


        direction = "LONG"


        if score.bearish:

            direction = "SHORT"



        trade = create_trade(
            symbol=symbol,

            df=df,

            account_balance=
                self.session.portfolio.account_balance,

            risk_percent=1.0,

            direction=direction,

            confidence=score.confidence,
        )



        if trade:

            self.trades.save(
                trade
            )


            self.session.portfolio.add_trade(
                trade
            )


            self.portfolio_repository.save(
                self.session.portfolio
            )


            self.journal.log(
                "TRADE_CREATED",
                trade.symbol
            )


        return score, trade



    def monitor_trades(
        self
    ):

        open_trades = self.trades.open_trades()


        prices = {}


        for trade in open_trades:

            df = self.market.get_history(
                trade.symbol
            )


            prices[
                trade.symbol
            ] = float(
                df["Close"].iloc[-1]
            )


        return self.execution.monitor_open_trades(
            open_trades,
            prices
        )



    def history(self):

        return self.trades.recent(
            20
        )



    def performance(self):

        return self.performance_tracker.calculate()



    def portfolio(self):

        return self.session.portfolio



    def close(self):

        self.database.close()