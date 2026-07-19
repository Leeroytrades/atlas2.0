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


class AtlasEngine:

    def __init__(self):

        self.session = Session()

        self.market = MarketData()

        self.scanner = Scanner()

    def scan_market(self):

        return self.scanner.scan(
            self.session.watchlist.all()
        )

    def analyse(self, symbol: str):

        df = self.market.get_history(symbol)

        df = build_indicator_set(df)

        score = generate_scorecard(df)

        direction = "LONG"

        if score.bearish:
            direction = "SHORT"

        trade = create_trade(
            symbol=symbol,
            df=df,
            account_balance=self.session.portfolio.account_balance,
            risk_percent=1.0,
            direction=direction,
            confidence=score.confidence,
        )

        return score, trade

    def best_trade(self):

        scans = self.scan_market()

        if not scans:
            return None

        best = scans[0]

        score, trade = self.analyse(best.symbol)

        return best, score, trade