"""
Atlas AI Trading Assistant 2.3

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
- Smart opportunity selection
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



class AtlasEngine:


    def __init__(self):


        # -------------------------
        # Database
        # -------------------------

        self.database = Database()



        # -------------------------
        # Session
        # -------------------------

        self.session = Session()



        # -------------------------
        # Scanner
        # -------------------------

        self.scanner = Scanner()



        # -------------------------
        # Repositories
        # -------------------------

        self.trade_repository = TradeRepository(
            self.database
        )


        self.equity_history_repository = EquityHistoryRepository(
            self.database
        )


        self.journal = JournalRepository(
            self.database
        )



        # -------------------------
        # Risk
        # -------------------------

        self.position_manager = PositionManager(
            self.trade_repository
        )



        # -------------------------
        # Monitoring
        # -------------------------

        self.trade_monitor = TradeMonitor(
            self.trade_repository,
            self.journal
        )



        # -------------------------
        # Performance
        # -------------------------

        self.performance_service = PerformanceService(
            self.trade_repository
        )



        self.load_portfolio()



    # =====================================================
    # MARKET SCAN
    # =====================================================

    def scan_market(self):

        return self.scanner.scan(
            self.session.watchlist.symbols
        )



    # =====================================================
    # SMART OPPORTUNITY FINDER
    # =====================================================

    def find_opportunity(
        self,
        scans
    ):


        opportunities = []


        for score in scans:


            if score.bias != "BUY":

                continue



            if self.position_manager.has_open_position(
                score.symbol
            ):

                print(
                    f"{score.symbol}: Existing position - skipped"
                )

                continue



            opportunities.append(score)



        if not opportunities:

            return None



        opportunities.sort(
            key=lambda x: x.confidence,
            reverse=True
        )



        opportunity = opportunities[0]



        print()

        print(
            f"Trade opportunity found: {opportunity.symbol}"
        )



        return opportunity



    # =====================================================
    # ANALYSE SYMBOL
    # =====================================================

    def analyse(
        self,
        symbol,
        scans=None
    ):


        if scans is None:

            scans = self.scan_market()



        score = next(

            (
                item

                for item in scans

                if item.symbol == symbol

            ),

            None

        )



        if score is None:

            return None, None



        trade = None



        if score.bias == "BUY":


            if not self.position_manager.has_open_position(
                symbol
            ):


                trade = create_trade(

                    symbol,

                    score.dataframe,

                    self.session.portfolio.account_balance,

                    1.0,

                    "LONG",

                    score.confidence / 100

                )



                if trade:


                    self.trade_repository.save(
                        trade
                    )


                    self.session.portfolio.add_trade(
                        trade
                    )


                    print(
                        f"Trade created: {symbol}"
                    )



        return score, trade



    # =====================================================
    # SEARCH AND TRADE
    # =====================================================

    def search_and_trade(
        self,
        scans
    ):


        opportunity = self.find_opportunity(
            scans
        )



        if opportunity is None:

            return None



        _, trade = self.analyse(

            opportunity.symbol,

            scans

        )


        return trade



    # =====================================================
    # PORTFOLIO
    # =====================================================

    def portfolio(self):

        return self.session.portfolio



    def load_portfolio(self):


        trades = self.trade_repository.open_trades()



        for trade in trades:


            self.session.portfolio.add_trade(
                trade
            )



    # =====================================================
    # PERFORMANCE
    # =====================================================

    def performance(self):


        metrics = self.performance_service.summary()



        equity = metrics.get(

            "equity",

            self.session.portfolio.account_balance

        )



        latest = self.equity_history_repository.latest()



        last_equity = None



        if latest:

            last_equity = latest["equity"]



        if last_equity != equity:


            self.equity_history_repository.save(
                equity
            )



        return metrics



    # =====================================================
    # EQUITY HISTORY
    # =====================================================

    def equity_history(self):

        return self.equity_history_repository.all()



    # =====================================================
    # TRADE MONITOR
    # =====================================================

    def monitor_trades(self):


        trades = self.trade_repository.open_trades()



        results = []



        for trade in trades:


            try:


                current_price = self.scanner.market.get_price(
                    trade.symbol
                )


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

                    "price": current_price,

                }

            )



        return results



    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.database.close()