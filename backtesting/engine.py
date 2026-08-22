"""
Atlas AI Trading Platform 4.4

Backtesting Engine

Responsible for:

- Running strategies over historical data
- Creating trades
- ATR-based stop/target configuration
- Simulating trade lifecycle
- Commission
- Slippage
- Breakeven protection
- Maximum holding period
- Minimum spacing between trades
- Trade statistics
- Equity curve
- Drawdown

Execution rules:

1. Signal generated at candle N enters at candle N+1 OPEN.

2. Only ONE position may be open at a time.

3. A new signal is ignored while the previous simulated
   trade is still open.

4. A minimum number of candles must separate the previous
   trade exit from the next eligible signal.

5. ATR used for position sizing and ATR used by the simulator
   come from the same entry candle.

6. Locked ATR stop/target parameters are applied consistently
   to Trade creation and simulation.

7. If stop and target are both touched during the same candle,
   STOP wins.
"""

from __future__ import annotations

from risk.risk_manager import create_trade

from backtesting.simulator import Simulator

from strategy.config import StrategyConfig


class BacktestEngine:

    def __init__(
        self,
        starting_cash: float = 100000.0,
        minimum_score=None,
        minimum_confidence=None,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
        commission: float = 1.0,
        slippage: float = 0.01,
        max_hold: int = 100,
        min_candles_between_trades=None,
    ):

        self.starting_cash = float(
            starting_cash
        )

        # ----------------------------------------------------
        # These are optional optimiser/backtest overrides.
        #
        # StrategyConfig still provides the minimum floor.
        # ----------------------------------------------------

        self.minimum_score = (
            None
            if minimum_score is None
            else float(minimum_score)
        )

        self.minimum_confidence = (
            None
            if minimum_confidence is None
            else float(minimum_confidence)
        )

        self.atr_stop = float(
            atr_stop
        )

        self.atr_target = float(
            atr_target
        )

        self.commission = float(
            commission
        )

        self.slippage = float(
            slippage
        )

        self.max_hold = int(
            max_hold
        )

        if min_candles_between_trades is None:

            min_candles_between_trades = (
                StrategyConfig.MIN_CANDLES_BETWEEN_TRADES
            )

        self.min_candles_between_trades = max(
            0,
            int(
                min_candles_between_trades
            ),
        )

    # ========================================================
    # EMPTY RESULTS
    # ========================================================

    def _empty_results(self):

        return {

            "starting_cash":
                self.starting_cash,

            "ending_equity":
                self.starting_cash,

            "profit":
                0.0,

            "net_profit":
                0.0,

            "total_trades":
                0,

            "trades":
                0,

            "wins":
                0,

            "losses":
                0,

            "win_rate":
                0.0,

            "profit_factor":
                0.0,

            "average_trade":
                0.0,

            "max_drawdown":
                0.0,

            "trade_list":
                [],

        }

    # ========================================================
    # RUN
    # ========================================================

    def run(
        self,
        symbol: str,
        dataframe,
    ):

        if (
            dataframe is None
            or len(dataframe) < 50
        ):

            return self._empty_results()

        # ----------------------------------------------------
        # Import here to avoid circular imports
        # ----------------------------------------------------

        from strategy.runner import StrategyRunner

        # ----------------------------------------------------
        # Strategy runner
        #
        # It performs:
        #
        #   regime filtering
        #   strategy routing
        #   score filtering
        #   confidence filtering
        #
        # The engine therefore does NOT duplicate those rules.
        # ----------------------------------------------------

        runner = StrategyRunner(

            score_threshold=
                self.minimum_score,

            confidence_threshold=
                self.minimum_confidence,

        )

        # ----------------------------------------------------
        # Simulator
        # ----------------------------------------------------

        simulator = Simulator(

            starting_cash=
                self.starting_cash,

            commission=
                self.commission,

            slippage=
                self.slippage,

            atr_stop=
                self.atr_stop,

            atr_target=
                self.atr_target,

            max_hold=
                self.max_hold,

        )

        # ====================================================
        # DIAGNOSTICS
        # ====================================================

        candles_processed = 0

        raw_signals = 0

        actionable_signals = 0

        rejected_direction = 0

        trade_spacing_rejections = 0

        trade_creation_failures = 0

        successful_trades = 0

        runner_failures = 0

        first_trade_error = None

        # ====================================================
        # SINGLE-POSITION WALK
        # ====================================================

        index = 49

        # ----------------------------------------------------
        # Last trade exit candle.
        #
        # None means no trade has occurred yet.
        # ----------------------------------------------------

        last_exit_index = None

        while index < (
            len(dataframe) - 1
        ):

            candles_processed += 1

            # =================================================
            # HISTORICAL WINDOW
            #
            # Strategy sees candles only through N.
            # =================================================

            historical = dataframe.iloc[
                :index + 1
            ].copy()

            # =================================================
            # RUN STRATEGY
            # =================================================

            try:

                signal = runner.run(

                    dataframe=
                        historical,

                    symbol=
                        symbol,

                )

            except Exception as exc:

                runner_failures += 1

                if first_trade_error is None:

                    first_trade_error = exc

                index += 1

                continue

            # =================================================
            # NO SIGNAL
            # =================================================

            if signal is None:

                index += 1

                continue

            raw_signals += 1

            # =================================================
            # NORMALISE SIGNAL
            # =================================================

            if isinstance(
                signal,
                dict,
            ):

                direction = signal.get(
                    "signal",
                    "HOLD",
                )

            else:

                direction = getattr(
                    signal,
                    "signal",
                    "HOLD",
                )

            if isinstance(
                direction,
                str,
            ):

                direction = (
                    direction
                    .upper()
                    .strip()
                )

            # =================================================
            # DIRECTION
            # =================================================

            if direction not in (
                "BUY",
                "SELL",
            ):

                rejected_direction += 1

                index += 1

                continue

            # =================================================
            # MINIMUM TRADE SPACING
            #
            # If the previous trade exited on candle 117 and
            # the configured spacing is 20, the next eligible
            # signal candle is 138.
            #
            # Formula:
            #
            #   signal_index >=
            #       last_exit_index
            #       + minimum_gap
            #       + 1
            # =================================================

            if last_exit_index is not None:

                earliest_allowed = (

                    last_exit_index
                    + self.min_candles_between_trades
                    + 1

                )

                if index < earliest_allowed:

                    trade_spacing_rejections += 1

                    index += 1

                    continue

            actionable_signals += 1

            # =================================================
            # ENTRY
            #
            # Signal at N
            # Entry at N+1 OPEN
            # =================================================

            entry_index = (
                index + 1
            )

            if entry_index >= len(
                dataframe
            ):

                break

            try:

                entry_price = float(
                    dataframe[
                        "Open"
                    ].iloc[
                        entry_index
                    ]
                )

            except (
                KeyError,
                TypeError,
                ValueError,
            ):

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "Entry candle OPEN "
                        "could not be read"
                    )

                index += 1

                continue

            if entry_price <= 0:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "Entry price was not positive"
                    )

                index += 1

                continue

            # =================================================
            # TRADE DIRECTION
            # =================================================

            trade_direction = (

                "LONG"
                if direction == "BUY"
                else "SHORT"

            )

            # =================================================
            # SIGNAL METADATA
            # =================================================

            if isinstance(
                signal,
                dict,
            ):

                confidence = float(
                    signal.get(
                        "confidence",
                        0.0,
                    )
                )

                strategy_name = signal.get(
                    "strategy",
                    "UNKNOWN",
                )

            else:

                confidence = float(
                    getattr(
                        signal,
                        "confidence",
                        0.0,
                    )
                )

                strategy_name = getattr(
                    signal,
                    "strategy",
                    "UNKNOWN",
                )

            # =================================================
            # CREATE TRADE
            #
            # CRITICAL:
            #
            # entry_index is exactly the same index passed to
            # Simulator.
            #
            # Therefore the risk manager and simulator use
            # the same entry candle ATR.
            # =================================================

            try:

                trade = create_trade(

                    symbol=
                        symbol,

                    direction=
                        trade_direction,

                    entry=
                        entry_price,

                    dataframe=
                        dataframe,

                    index=
                        entry_index,

                    account_balance=
                        simulator.cash,

                    risk_percent=
                        1.0,

                    confidence=
                        confidence,

                    atr_stop=
                        self.atr_stop,

                    atr_target=
                        self.atr_target,

                )

            except Exception as exc:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = exc

                index += 1

                continue

            # =================================================
            # CREATE FAILURE
            # =================================================

            if trade is None:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "create_trade returned None"
                    )

                index += 1

                continue

            # =================================================
            # ENTRY CONSISTENCY
            # =================================================

            if abs(
                float(trade.entry)
                -
                entry_price
            ) > 1e-9:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "Trade entry does not match "
                        "next candle OPEN"
                    )

                index += 1

                continue

            # =================================================
            # STRATEGY ATTRIBUTION
            # =================================================

            try:

                trade.strategy = (

                    strategy_name
                    if strategy_name
                    else "UNKNOWN"

                )

            except Exception:

                pass

            # =================================================
            # SIMULATE
            # =================================================

            simulated = simulator.simulate_trade(

                trade,

                dataframe,

                entry_index,

            )

            if simulated is None:

                index += 1

                continue

            successful_trades += 1

            last_exit_index = (
                simulated.exit_index
            )

            # =================================================
            # NEXT ELIGIBLE SIGNAL
            #
            # First move past the exit candle.
            #
            # The spacing rule above will then prevent entries
            # until the configured gap has elapsed.
            # =================================================

            index = (
                simulated.exit_index + 1
            )

        # ====================================================
        # DIAGNOSTICS
        # ====================================================

        print()

        print(
            "BACKTEST DIAGNOSTICS"
        )

        print(
            f"Candles processed: "
            f"{candles_processed}"
        )

        print(
            f"Raw signals: "
            f"{raw_signals}"
        )

        print(
            f"Actionable signals: "
            f"{actionable_signals}"
        )

        print(
            f"Rejected by direction: "
            f"{rejected_direction}"
        )

        print(
            f"Rejected by trade spacing: "
            f"{trade_spacing_rejections}"
        )

        print(
            f"Trade creation failures: "
            f"{trade_creation_failures}"
        )

        print(
            f"Successful trades: "
            f"{successful_trades}"
        )

        print(
            f"Strategy runner failures: "
            f"{runner_failures}"
        )

        print(
            f"Minimum candles between trades: "
            f"{self.min_candles_between_trades}"
        )

        if first_trade_error is not None:

            print()

            print(
                "FIRST ERROR:"
            )

            print(
                f"{type(first_trade_error).__name__}: "
                f"{first_trade_error}"
            )

        # ====================================================
        # ZERO TRADE WARNING
        # ====================================================

        if successful_trades == 0:

            print()

            print(
                "WARNING: BACKTEST PRODUCED "
                "ZERO TRADES"
            )

            if (
                actionable_signals > 0
                and trade_creation_failures > 0
            ):

                print(
                    "Signals passed filters but "
                    "trade creation failed."
                )

            elif raw_signals == 0:

                print(
                    "No strategy signals were "
                    "generated."
                )

        # ====================================================
        # RESULTS
        # ====================================================

        return simulator.results()