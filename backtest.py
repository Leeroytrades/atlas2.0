
"""
Atlas AI Trading Platform 4.2

Standalone Backtest Runner + Trade Analysis

Usage:

    python backtest.py SPY

Pipeline:

    MarketData
        ↓
    Historical OHLCV
        ↓
    Indicator Set
        ↓
    BacktestEngine
        ↓
    Trade Analysis
        ↓
    Performance Summary
"""

from __future__ import annotations

import sys
from collections import defaultdict

from backtesting.engine import BacktestEngine
from data.market_data import MarketData
from indicators.composite import build_indicator_set
from config.settings import settings


# ============================================================
# FORMATTING HELPERS
# ============================================================


def money(value: float) -> str:

    return f"${value:,.2f}"


def percent(value: float) -> str:

    return f"{value:.2f}%"


def print_section(title: str) -> None:

    print()
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)
    print()


# ============================================================
# TRADE ANALYSIS
# ============================================================


def analyse_trades(trades) -> None:

    if not trades:

        print_section("TRADE ANALYSIS")

        print("No completed trades to analyse.")
        print()

        return

    # ========================================================
    # BASIC GROUPS
    # ========================================================

    winners = [
        trade
        for trade in trades
        if trade.profit_loss > 0
    ]

    losers = [
        trade
        for trade in trades
        if trade.profit_loss < 0
    ]

    breakeven = [
        trade
        for trade in trades
        if trade.profit_loss == 0
    ]

    longs = [
        trade
        for trade in trades
        if trade.direction == "LONG"
    ]

    shorts = [
        trade
        for trade in trades
        if trade.direction == "SHORT"
    ]

    # ========================================================
    # EXIT REASONS
    # ========================================================

    exit_groups = defaultdict(list)

    for trade in trades:

        exit_groups[
            trade.exit_reason
        ].append(trade)

    # ========================================================
    # STRATEGIES
    # ========================================================

    strategy_groups = defaultdict(list)

    for trade in trades:

        strategy = (
            getattr(
                trade,
                "strategy",
                "UNKNOWN",
            )
            or
            "UNKNOWN"
        )

        strategy_groups[
            strategy
        ].append(trade)

    # ========================================================
    # CORE STATISTICS
    # ========================================================

    total_profit = sum(
        trade.profit_loss
        for trade in trades
    )

    gross_profit = sum(
        trade.profit_loss
        for trade in winners
    )

    gross_loss = abs(
        sum(
            trade.profit_loss
            for trade in losers
        )
    )

    average_winner = (
        gross_profit / len(winners)
        if winners
        else 0.0
    )

    average_loser = (
        gross_loss / len(losers)
        if losers
        else 0.0
    )

    average_hold = (
        sum(
            trade.candles_held
            for trade in trades
        )
        /
        len(trades)
    )

    largest_winner = max(
        winners,
        key=lambda trade: trade.profit_loss,
        default=None,
    )

    largest_loser = min(
        losers,
        key=lambda trade: trade.profit_loss,
        default=None,
    )

    # ========================================================
    # MAIN SUMMARY
    # ========================================================

    print_section("TRADE ANALYSIS")

    print(
        f"Total trades:          {len(trades)}"
    )

    print(
        f"Winners:               {len(winners)}"
    )

    print(
        f"Losers:                {len(losers)}"
    )

    print(
        f"Breakeven:             {len(breakeven)}"
    )

    print(
        f"Total realised P/L:    {money(total_profit)}"
    )

    print(
        f"Gross profit:          {money(gross_profit)}"
    )

    print(
        f"Gross loss:            {money(gross_loss)}"
    )

    print(
        f"Average winner:        {money(average_winner)}"
    )

    print(
        f"Average loser:         {money(-average_loser)}"
    )

    print(
        f"Average holding:       {average_hold:.2f} candles"
    )

    if largest_winner is not None:

        print(
            f"Largest winner:        "
            f"{money(largest_winner.profit_loss)}"
        )

    if largest_loser is not None:

        print(
            f"Largest loser:         "
            f"{money(largest_loser.profit_loss)}"
        )

    # ========================================================
    # LONG / SHORT
    # ========================================================

    print_section("LONG vs SHORT")

    for direction, group in (
        ("LONG", longs),
        ("SHORT", shorts),
    ):

        if not group:

            print(
                f"{direction}: no trades"
            )

            continue

        wins = [
            trade
            for trade in group
            if trade.profit_loss > 0
        ]

        losses = [
            trade
            for trade in group
            if trade.profit_loss < 0
        ]

        profit = sum(
            trade.profit_loss
            for trade in group
        )

        gross_profit_direction = sum(
            trade.profit_loss
            for trade in wins
        )

        gross_loss_direction = abs(
            sum(
                trade.profit_loss
                for trade in losses
            )
        )

        if gross_loss_direction > 0:

            profit_factor = (
                gross_profit_direction
                /
                gross_loss_direction
            )

        else:

            profit_factor = 0.0

        win_rate = (
            len(wins)
            /
            len(group)
            *
            100
        )

        print(
            f"{direction}"
        )

        print(
            f"  Trades:        {len(group)}"
        )

        print(
            f"  Wins:          {len(wins)}"
        )

        print(
            f"  Losses:        {len(losses)}"
        )

        print(
            f"  Win rate:      {percent(win_rate)}"
        )

        print(
            f"  Profit:        {money(profit)}"
        )

        print(
            f"  Profit factor: {profit_factor:.2f}"
        )

        print()

    # ========================================================
    # EXIT REASONS
    # ========================================================

    print_section("EXIT REASONS")

    for reason in sorted(exit_groups):

        group = exit_groups[reason]

        profit = sum(
            trade.profit_loss
            for trade in group
        )

        wins = sum(
            1
            for trade in group
            if trade.profit_loss > 0
        )

        losses_count = sum(
            1
            for trade in group
            if trade.profit_loss < 0
        )

        print(
            f"{reason}"
        )

        print(
            f"  Trades:   {len(group)}"
        )

        print(
            f"  Wins:     {wins}"
        )

        print(
            f"  Losses:   {losses_count}"
        )

        print(
            f"  P/L:      {money(profit)}"
        )

        print()

    # ========================================================
    # STRATEGY PERFORMANCE
    # ========================================================

    print_section("STRATEGY PERFORMANCE")

    for strategy in sorted(strategy_groups):

        group = strategy_groups[strategy]

        wins = [
            trade
            for trade in group
            if trade.profit_loss > 0
        ]

        losses = [
            trade
            for trade in group
            if trade.profit_loss < 0
        ]

        profit = sum(
            trade.profit_loss
            for trade in group
        )

        gross_strategy_profit = sum(
            trade.profit_loss
            for trade in wins
        )

        gross_strategy_loss = abs(
            sum(
                trade.profit_loss
                for trade in losses
            )
        )

        if gross_strategy_loss > 0:

            strategy_pf = (
                gross_strategy_profit
                /
                gross_strategy_loss
            )

        else:

            strategy_pf = 0.0

        win_rate = (
            len(wins)
            /
            len(group)
            *
            100
        )

        contribution = (
            profit
            /
            total_profit
            *
            100
            if total_profit != 0
            else 0.0
        )

        print(
            f"{strategy}"
        )

        print(
            f"  Trades:          {len(group)}"
        )

        print(
            f"  Wins:            {len(wins)}"
        )

        print(
            f"  Losses:          {len(losses)}"
        )

        print(
            f"  Win rate:        {percent(win_rate)}"
        )

        print(
            f"  Profit:          {money(profit)}"
        )

        print(
            f"  Profit factor:   {strategy_pf:.2f}"
        )

        print(
            f"  Profit share:    {percent(contribution)}"
        )

        print()

    # ========================================================
    # PROFIT CONCENTRATION
    # ========================================================

    print_section("PROFIT CONCENTRATION")

    sorted_winners = sorted(
        winners,
        key=lambda trade: trade.profit_loss,
        reverse=True,
    )

    if sorted_winners and total_profit > 0:

        top_1_profit = sorted_winners[0].profit_loss

        top_3_profit = sum(
            trade.profit_loss
            for trade in sorted_winners[:3]
        )

        top_5_profit = sum(
            trade.profit_loss
            for trade in sorted_winners[:5]
        )

        print(
            f"Top 1 winning trade: "
            f"{money(top_1_profit)}"
        )

        print(
            f"Top 1 contribution:   "
            f"{percent(top_1_profit / total_profit * 100)}"
        )

        print()

        print(
            f"Top 3 winning trades: "
            f"{money(top_3_profit)}"
        )

        print(
            f"Top 3 contribution:   "
            f"{percent(top_3_profit / total_profit * 100)}"
        )

        print()

        print(
            f"Top 5 winning trades: "
            f"{money(top_5_profit)}"
        )

        print(
            f"Top 5 contribution:   "
            f"{percent(top_5_profit / total_profit * 100)}"
        )

        print()

        if (
            top_1_profit / total_profit
            >= 0.50
        ):

            print(
                "WARNING: More than 50% of total "
                "profit comes from one trade."
            )

        elif (
            top_3_profit / total_profit
            >= 0.75
        ):

            print(
                "WARNING: More than 75% of total "
                "profit comes from the top three trades."
            )

        else:

            print(
                "Profit concentration does not "
                "appear extreme."
            )

    else:

        print(
            "Insufficient positive profit "
            "for concentration analysis."
        )

    # ========================================================
    # INDIVIDUAL TRADES
    # ========================================================

    print_section("ALL TRADES")

    print(
        " # | Direction | Strategy | Entry | Exit | "
        "P/L | Result | Exit Reason | Held"
    )

    print("-" * 100)

    for number, trade in enumerate(
        trades,
        start=1,
    ):

        strategy = (
            getattr(
                trade,
                "strategy",
                "UNKNOWN",
            )
            or
            "UNKNOWN"
        )

        print(
            f"{number:2d} | "
            f"{trade.direction:<9} | "
            f"{strategy:<16} | "
            f"{trade.entry:>7.2f} | "
            f"{trade.exit:>7.2f} | "
            f"{trade.profit_loss:>9.2f} | "
            f"{trade.result:<10} | "
            f"{trade.exit_reason:<16} | "
            f"{trade.candles_held:>4}"
        )

    print()


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    # ========================================================
    # ARGUMENTS
    # ========================================================

    if len(sys.argv) < 2:

        print()
        print("Usage: python backtest.py SYMBOL")
        print()
        print("Example: python backtest.py SPY")
        print()

        return

    symbol = sys.argv[1].upper().strip()

    # ========================================================
    # HEADER
    # ========================================================

    print()
    print("=================================")
    print(" Atlas Backtest")
    print(" Symbol:", symbol)
    print("=================================")
    print()

    # ========================================================
    # MARKET DATA
    # ========================================================

    market_data = MarketData()

    period = settings.data.default_period
    interval = settings.data.default_interval

    print("Loading historical data...")
    print(
        f"Period: {period}"
    )
    print(
        f"Interval: {interval}"
    )
    print()

    try:

        dataframe = market_data.get_history(
            symbol=symbol,
            period=period,
            interval=interval,
            use_cache=True,
        )

    except Exception as exc:

        print()
        print("ERROR: Failed to load market data.")
        print(
            f"{type(exc).__name__}: {exc}"
        )
        print()

        return

    if dataframe is None or dataframe.empty:

        print()
        print("ERROR: No historical data returned.")
        print()

        return

    print(
        f"Downloaded candles: {len(dataframe)}"
    )

    print(
        f"Start: {dataframe.index[0]}"
    )

    print(
        f"End:   {dataframe.index[-1]}"
    )

    print()

    # ========================================================
    # INDICATORS
    # ========================================================

    print("Building indicators...")

    try:

        dataframe = build_indicator_set(
            dataframe
        )

    except Exception as exc:

        print()
        print("ERROR: Failed to build indicators.")
        print(
            f"{type(exc).__name__}: {exc}"
        )
        print()

        return

    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "ATR",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        print()
        print(
            "ERROR: Required indicator/data columns "
            "are missing."
        )

        print(
            "Missing:",
            ", ".join(missing_columns),
        )

        print()

        return

    print(
        f"Indicator columns: {len(dataframe.columns)}"
    )

    print()

    # ========================================================
    # BACKTEST ENGINE
    # ========================================================

    print("Running backtest...")
    print()

    engine = BacktestEngine()

    try:

        results = engine.run(
            symbol=symbol,
            dataframe=dataframe,
        )

    except Exception as exc:

        print()
        print("ERROR: Backtest failed.")
        print(
            f"{type(exc).__name__}: {exc}"
        )
        print()

        raise

    # ========================================================
    # RESULTS
    # ========================================================

    print_section("BACKTEST RESULTS")

    display_keys = [
        "starting_cash",
        "ending_equity",
        "net_profit",
        "profit",
        "total_trades",
        "wins",
        "losses",
        "win_rate",
        "profit_factor",
        "average_trade",
        "max_drawdown",
    ]

    for key in display_keys:

        if key not in results:
            continue

        value = results[key]

        if isinstance(value, float):

            print(
                f"{key}: {value:.2f}"
            )

        else:

            print(
                f"{key}: {value}"
            )

    # ========================================================
    # TRADE ANALYSIS
    # ========================================================

    trades = results.get(
        "trade_list",
        [],
    )

    analyse_trades(
        trades
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    print_section("BACKTEST COMPLETE")

    print(
        f"{symbol}: "
        f"{len(trades)} trades, "
        f"{money(results.get('net_profit', 0.0))} net profit, "
        f"PF {results.get('profit_factor', 0.0):.2f}, "
        f"DD {results.get('max_drawdown', 0.0):.2f}%"
    )

    print()


if __name__ == "__main__":

    main()