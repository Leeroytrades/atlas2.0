"""
Atlas AI Trading Platform 4.3

Backtesting Engine

Responsible for:

- Running strategies over historical data
- Applying score thresholds
- Applying confidence thresholds
- Creating trades
- ATR-based stop/target configuration
- Simulating trade lifecycle
- Commission
- Slippage
- Breakeven protection
- Maximum holding period
- Trade statistics
- Equity curve
- Drawdown

Important execution rules:

1. A signal generated at candle N is entered at candle N+1 OPEN.

2. Only ONE position may be open at a time.

3. A new signal is ignored while the previous simulated
   trade is still open.

4. ATR used for position sizing and ATR used by the simulator
   must come from the same entry candle.

5. Locked ATR stop/target parameters are applied consistently
   to both Trade creation and simulation.

6. Execution is deliberately conservative when both a stop
   and target are touched during the same candle.

   The STOP wins because OHLC data cannot determine which
   level was reached first.
"""

from __future__ import annotations

from models.trade import Trade

from risk.risk_manager import create_trade

from backtesting.simulator import Simulator


# ============================================================
# BACKTEST ENGINE
# ============================================================


class BacktestEngine:

    def __init__(
        self,
        starting_cash: float = 100000.0,
        minimum_score: int = 70,
        minimum_confidence: float = 0.70,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
        commission: float = 1.0,
        slippage: float = 0.01,
        max_hold: int = 100,
    ):

        self.starting_cash = float(
            starting_cash
        )

        self.minimum_score = int(
            minimum_score
        )

        self.minimum_confidence = float(
            minimum_confidence
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
            or
            len(dataframe) < 30
        ):

            return self._empty_results()

        # ----------------------------------------------------
        # Import here to avoid circular imports
        # ----------------------------------------------------

        from strategy.runner import StrategyRunner

        # ----------------------------------------------------
        # Strategy runner
        # ----------------------------------------------------

        runner = StrategyRunner(
            score_threshold=
                self.minimum_score,

            confidence_threshold=
                self.minimum_confidence,
        )

        # ----------------------------------------------------
        # Simulator
        #
        # IMPORTANT:
        #
        # This is the canonical Simulator from
        # backtesting.simulator.
        #
        # The engine does not contain its own simulator.
        #
        # The same locked ATR parameters are passed to the
        # simulator and to create_trade() below.
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

        rejected_score = 0

        rejected_confidence = 0

        trade_creation_failures = 0

        successful_trades = 0

        runner_failures = 0

        first_trade_error = None

        # ====================================================
        # SINGLE-POSITION WALK
        #
        # A signal generated at candle N enters at candle
        # N+1 OPEN.
        #
        # Once a trade is opened, index jumps to the candle
        # immediately after its exit.
        #
        # Therefore no new signal can be evaluated while a
        # simulated position is open.
        # ====================================================

        index = 20

        while index < (
            len(dataframe) - 1
        ):

            candles_processed += 1

            # ------------------------------------------------
            # HISTORICAL WINDOW
            #
            # Strategy sees only candles up to N.
            # ------------------------------------------------

            historical = dataframe.iloc[
                :index + 1
            ].copy()

            # ------------------------------------------------
            # RUN STRATEGY
            # ------------------------------------------------

            try:

                signal = runner.run(
                    dataframe=historical,
                    symbol=symbol,
                )

            except TypeError:

                try:

                    signal = runner.run(
                        historical,
                        symbol,
                    )

                except Exception as exc:

                    runner_failures += 1

                    if first_trade_error is None:

                        first_trade_error = exc

                    index += 1

                    continue

            except Exception as exc:

                runner_failures += 1

                if first_trade_error is None:

                    first_trade_error = exc

                index += 1

                continue

            # ------------------------------------------------
            # NO SIGNAL
            # ------------------------------------------------

            if signal is None:

                index += 1

                continue

            raw_signals += 1

            # ------------------------------------------------
            # NORMALISE SIGNAL
            # ------------------------------------------------

            if isinstance(
                signal,
                dict
            ):

                direction = signal.get(
                    "signal",
                    "HOLD"
                )

                score = float(
                    signal.get(
                        "score",
                        0
                    )
                )

                confidence = float(
                    signal.get(
                        "confidence",
                        0
                    )
                )

                strategy_name = signal.get(
                    "strategy",
                    "UNKNOWN"
                )

            else:

                direction = getattr(
                    signal,
                    "signal",
                    "HOLD"
                )

                score = float(
                    getattr(
                        signal,
                        "score",
                        0
                    )
                )

                confidence = float(
                    getattr(
                        signal,
                        "confidence",
                        0
                    )
                )

                strategy_name = getattr(
                    signal,
                    "strategy",
                    "UNKNOWN"
                )

            # ------------------------------------------------
            # NORMALISE DIRECTION
            # ------------------------------------------------

            if isinstance(
                direction,
                str
            ):

                direction = (
                    direction
                    .upper()
                    .strip()
                )

            # ------------------------------------------------
            # DIRECTION
            # ------------------------------------------------

            if direction not in (
                "BUY",
                "SELL",
            ):

                rejected_direction += 1

                index += 1

                continue

            # ------------------------------------------------
            # SCORE
            #
            # Use absolute score because BUY and SELL
            # strategies may encode direction using
            # positive/negative scores.
            # ------------------------------------------------

            if abs(
                score
            ) < self.minimum_score:

                rejected_score += 1

                index += 1

                continue

            # ------------------------------------------------
            # CONFIDENCE
            # ------------------------------------------------

            if confidence < (
                self.minimum_confidence
            ):

                rejected_confidence += 1

                index += 1

                continue

            actionable_signals += 1

            # =================================================
            # ENTRY
            #
            # Signal is generated at candle N.
            #
            # Execution occurs at candle N+1 OPEN.
            # =================================================

            entry_index = (
                index + 1
            )

            if entry_index >= len(
                dataframe
            ):

                break

            entry_price = float(
                dataframe[
                    "Open"
                ].iloc[
                    entry_index
                ]
            )

            if entry_price <= 0:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "Entry price was not positive"
                    )

                index += 1

                continue

            # ------------------------------------------------
            # CONVERT SIGNAL DIRECTION
            # ------------------------------------------------

            trade_direction = (
                "LONG"
                if direction == "BUY"
                else "SHORT"
            )

            # =================================================
            # CREATE TRADE
            #
            # IMPORTANT:
            #
            # Pass the exact entry price and exact entry candle
            # index into the risk manager.
            #
            # Therefore:
            #
            #   Entry
            #   ATR
            #   Stop
            #   Target
            #   Position size
            #
            # all refer to the same historical candle and
            # locked parameters.
            # =================================================

            try:

                trade = create_trade(

                    symbol=symbol,

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

            # ------------------------------------------------
            # CREATE TRADE FAILURE
            # ------------------------------------------------

            if trade is None:

                trade_creation_failures += 1

                if first_trade_error is None:

                    first_trade_error = (
                        "create_trade returned None"
                    )

                index += 1

                continue

            # =================================================
            # VERIFY ENTRY CONSISTENCY
            #
            # The Trade entry must exactly match the next
            # candle OPEN used by the backtest.
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
            #
            # IMPORTANT:
            #
            # entry_index is passed directly into the canonical
            # simulator.
            #
            # This guarantees the simulator reads ATR from the
            # exact same entry candle used by create_trade().
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

            # =================================================
            # CRITICAL SINGLE-POSITION RULE
            #
            # Do not evaluate another signal until the current
            # trade has exited.
            #
            # If:
            #
            #   entry_index = 101
            #   exit_index  = 117
            #
            # the next strategy evaluation occurs at:
            #
            #   index = 118
            #
            # This guarantees that only ONE position can be
            # open at any point in the backtest.
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
            f"Rejected by score: "
            f"{rejected_score}"
        )

        print(
            f"Rejected by confidence: "
            f"{rejected_confidence}"
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
            f"Single-position trades: "
            f"{successful_trades}"
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