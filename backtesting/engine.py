"""
Atlas AI Trading Platform 4.4

Backtesting Engine

Responsible for:

- Running strategies over historical data
- Applying StrategyRunner filters
- Creating trades
- ATR-based stop/target configuration
- Simulating trade lifecycle
- Commission
- Slippage
- Breakeven protection
- Maximum holding period
- Strategy attribution
- Trade statistics
- Equity curve
- Drawdown

Execution rules:

1. A signal generated at candle N is entered at candle N+1 OPEN.

2. Only ONE position may be open at a time.

3. A new signal is ignored while the previous simulated
   trade is still open.

4. ATR used for position sizing and ATR used by the simulator
   must come from the same entry candle.

5. Locked ATR stop/target parameters are applied consistently
   to both Trade creation and simulation.

6. Stop/target collisions are handled conservatively by the
   Simulator. STOP wins when both are touched on the same
   candle.

7. Strategy attribution is preserved from signal generation
   through Trade and SimulatedTrade.

8. StrategyRunner is the canonical signal quality gate.
"""

from __future__ import annotations

from backtesting.simulator import Simulator
from risk.risk_manager import create_trade


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
        breakeven_atr: float = 1.5,
    ):

        self.starting_cash = float(starting_cash)

        self.minimum_score = int(
            minimum_score
        )

        self.minimum_confidence = float(
            minimum_confidence
        )

        self.atr_stop = max(
            0.0,
            float(atr_stop),
        )

        self.atr_target = max(
            0.0,
            float(atr_target),
        )

        self.commission = max(
            0.0,
            float(commission),
        )

        self.slippage = max(
            0.0,
            float(slippage),
        )

        self.max_hold = max(
            1,
            int(max_hold),
        )

        self.breakeven_atr = max(
            0.0,
            float(breakeven_atr),
        )

    # ========================================================
    # EMPTY RESULTS
    # ========================================================

    def _empty_results(self):

        return {
            "starting_cash": round(
                self.starting_cash,
                2,
            ),
            "ending_equity": round(
                self.starting_cash,
                2,
            ),
            "profit": 0.0,
            "net_profit": 0.0,
            "total_trades": 0,
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "average_trade": 0.0,
            "max_drawdown": 0.0,
            "trade_list": [],
            "equity_curve": [
                self.starting_cash
            ],
        }

    # ========================================================
    # RUN
    # ========================================================

    def run(
        self,
        symbol: str,
        dataframe,
    ):
        """
        Run a backtest against one historical dataframe.

        Parameters
        ----------
        symbol:
            Market symbol being tested.

        dataframe:
            Historical OHLC dataframe containing at minimum:

                Open
                High
                Low
                Close

            and preferably:

                ATR
        """

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if dataframe is None:

            return self._empty_results()

        if len(dataframe) < 50:

            return self._empty_results()

        required_columns = {
            "Open",
            "High",
            "Low",
            "Close",
        }

        missing_columns = (
            required_columns
            -
            set(dataframe.columns)
        )

        if missing_columns:

            print(
                "BACKTEST ERROR: Missing columns: "
                f"{sorted(missing_columns)}"
            )

            return self._empty_results()

        # ----------------------------------------------------
        # Import here to avoid circular imports
        # ----------------------------------------------------

        from strategy.runner import StrategyRunner

        # ====================================================
        # STRATEGY RUNNER
        # ====================================================

        runner = StrategyRunner(
            score_threshold=self.minimum_score,
            confidence_threshold=self.minimum_confidence,
        )

        # ====================================================
        # CANONICAL SIMULATOR
        # ====================================================

        simulator = Simulator(
            starting_cash=self.starting_cash,
            commission=self.commission,
            slippage=self.slippage,
            atr_stop=self.atr_stop,
            atr_target=self.atr_target,
            max_hold=self.max_hold,
            breakeven_atr=self.breakeven_atr,
        )

        # ====================================================
        # DIAGNOSTICS
        # ====================================================

        candles_processed = 0
        runner_signals = 0
        actionable_signals = 0

        rejected_direction = 0
        rejected_score = 0
        rejected_confidence = 0

        trade_creation_failures = 0
        successful_trades = 0
        runner_failures = 0
        simulation_failures = 0

        first_error = None

        # ====================================================
        # SINGLE POSITION WALK
        #
        # Signal at N
        #
        # Entry at N+1 OPEN
        #
        # After exit:
        #
        # Resume at exit + 1
        # ====================================================

        index = 50

        while index < len(dataframe) - 1:

            candles_processed += 1

            # =================================================
            # HISTORICAL WINDOW
            # =================================================

            historical = dataframe.iloc[
                :index + 1
            ].copy()

            # =================================================
            # RUN STRATEGY
            # =================================================

            try:

                signal = runner.run(
                    dataframe=historical,
                    symbol=symbol,
                )

            except Exception as exc:

                runner_failures += 1

                if first_error is None:
                    first_error = exc

                index += 1
                continue

            # =================================================
            # NO SIGNAL
            # =================================================

            if signal is None:

                index += 1
                continue

            runner_signals += 1

            # =================================================
            # NORMALISE SIGNAL
            # =================================================

            if isinstance(signal, dict):

                direction = signal.get(
                    "signal",
                    "HOLD",
                )

                score = signal.get(
                    "score",
                    0.0,
                )

                confidence = signal.get(
                    "confidence",
                    0.0,
                )

                strategy_name = signal.get(
                    "strategy",
                    signal.get(
                        "selected_strategy",
                        "UNKNOWN",
                    ),
                )

            else:

                direction = getattr(
                    signal,
                    "signal",
                    "HOLD",
                )

                score = getattr(
                    signal,
                    "score",
                    0.0,
                )

                confidence = getattr(
                    signal,
                    "confidence",
                    0.0,
                )

                strategy_name = getattr(
                    signal,
                    "strategy",
                    "UNKNOWN",
                )

            # =================================================
            # NUMERIC SAFETY
            # =================================================

            try:

                score = float(score)

            except (
                TypeError,
                ValueError,
            ):

                score = 0.0

            try:

                confidence = float(
                    confidence
                )

            except (
                TypeError,
                ValueError,
            ):

                confidence = 0.0

            # =================================================
            # NORMALISE DIRECTION
            # =================================================

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
            # SCORE
            # =================================================

            if abs(score) < self.minimum_score:

                rejected_score += 1

                index += 1
                continue

            # =================================================
            # CONFIDENCE
            # =================================================

            if confidence < self.minimum_confidence:

                rejected_confidence += 1

                index += 1
                continue

            actionable_signals += 1

            # =================================================
            # ENTRY CANDLE
            #
            # Signal at N.
            # Entry at N+1 OPEN.
            # =================================================

            entry_index = index + 1

            if entry_index >= len(dataframe):

                break

            # =================================================
            # ENTRY PRICE
            # =================================================

            try:

                entry_price = float(
                    dataframe[
                        "Open"
                    ].iloc[
                        entry_index
                    ]
                )

            except (
                TypeError,
                ValueError,
                IndexError,
            ):

                trade_creation_failures += 1

                if first_error is None:
                    first_error = (
                        "Unable to read entry candle OPEN"
                    )

                index += 1
                continue

            if entry_price <= 0:

                trade_creation_failures += 1

                if first_error is None:
                    first_error = (
                        "Entry price was not positive"
                    )

                index += 1
                continue

            # =================================================
            # SIGNAL → TRADE DIRECTION
            # =================================================

            trade_direction = (
                "LONG"
                if direction == "BUY"
                else "SHORT"
            )

            # =================================================
            # CREATE TRADE
            #
            # CRITICAL:
            #
            # ATR is read from entry_index.
            # The Simulator receives the exact same index.
            # =================================================

            try:

                trade = create_trade(
                    symbol=symbol,
                    direction=trade_direction,
                    entry=entry_price,
                    dataframe=dataframe,
                    index=entry_index,
                    account_balance=simulator.cash,
                    risk_percent=1.0,
                    confidence=confidence,
                    atr_stop=self.atr_stop,
                    atr_target=self.atr_target,
                )

            except Exception as exc:

                trade_creation_failures += 1

                if first_error is None:
                    first_error = exc

                index += 1
                continue

            # =================================================
            # TRADE CREATION FAILURE
            # =================================================

            if trade is None:

                trade_creation_failures += 1

                if first_error is None:
                    first_error = (
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

                if first_error is None:
                    first_error = (
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
                    str(strategy_name).strip()
                    if strategy_name
                    else "UNKNOWN"
                )

            except Exception:

                trade.strategy = "UNKNOWN"

            # =================================================
            # SIMULATE
            # =================================================

            try:

                simulated = simulator.simulate_trade(
                    trade,
                    dataframe,
                    entry_index,
                )

            except Exception as exc:

                simulation_failures += 1

                if first_error is None:
                    first_error = exc

                index += 1
                continue

            # =================================================
            # SIMULATION FAILURE
            # =================================================

            if simulated is None:

                simulation_failures += 1

                index += 1
                continue

            successful_trades += 1

            # =================================================
            # SINGLE POSITION RULE
            # =================================================

            try:

                exit_index = int(
                    getattr(
                        simulated,
                        "exit_index",
                        entry_index,
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                exit_index = entry_index

            if exit_index < entry_index:
                exit_index = entry_index

            index = exit_index + 1

        # ====================================================
        # DIAGNOSTICS
        # ====================================================

        print()
        print("BACKTEST DIAGNOSTICS")
        print("--------------------")

        print(
            f"Symbol: {symbol}"
        )

        print(
            f"Candles processed: "
            f"{candles_processed}"
        )

        print(
            f"Runner signals: "
            f"{runner_signals}"
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
            f"Simulation failures: "
            f"{simulation_failures}"
        )

        print(
            f"Successful trades: "
            f"{successful_trades}"
        )

        print(
            f"Strategy runner failures: "
            f"{runner_failures}"
        )

        # ====================================================
        # RUNNER DIAGNOSTICS
        # ====================================================

        try:

            runner_stats = runner.statistics()

            print()
            print("STRATEGY RUNNER")
            print("----------------")

            print(
                f"Total windows: "
                f"{runner_stats.get('total_windows', 0)}"
            )

            print(
                f"Regime blocked: "
                f"{runner_stats.get('regime_blocked', 0)}"
            )

            print(
                f"Strategy attempts: "
                f"{runner_stats.get('strategy_attempts', 0)}"
            )

            print(
                f"Signals generated: "
                f"{runner_stats.get('signals_generated', 0)}"
            )

            print(
                f"Score rejected: "
                f"{runner_stats.get('signals_rejected_score', 0)}"
            )

            print(
                f"Confidence rejected: "
                f"{runner_stats.get('signals_rejected_confidence', 0)}"
            )

            print(
                f"Regimes: "
                f"{runner_stats.get('regimes', {})}"
            )

        except Exception:
            pass

        # ====================================================
        # FIRST ERROR
        # ====================================================

        if first_error is not None:

            print()
            print("FIRST ERROR:")

            print(
                f"{type(first_error).__name__}: "
                f"{first_error}"
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

            elif (
                actionable_signals > 0
                and simulation_failures > 0
            ):

                print(
                    "Signals passed filters but "
                    "simulation failed."
                )

            elif runner_signals == 0:

                print(
                    "No strategy signals were "
                    "generated."
                )

        # ====================================================
        # RESULTS
        # ====================================================

        return simulator.results()