"""
Atlas AI Trading Platform 4.2

Walk Forward Validation Engine

Workflow:

        Historical Data
                |
        Create Windows
                |
        Optimise Training Window
                |
        Lock Parameters
                |
        Run Unseen Validation Window
                |
        Calculate Validation Metrics
                |
        Detailed Trade Diagnostics
                |
        Apply Robustness / Acceptance Rules
                |
        PASS / PASS_LOW_SAMPLE / FAIL

This version adds detailed validation diagnostics so that failed
walk-forward windows can be investigated rather than simply
classified as PASS or FAIL.

Atlas 4.2 diagnostic improvements:

- Prints every validation trade individually
- Shows entry and exit prices
- Shows direction
- Shows strategy
- Shows P/L
- Shows exit reason
- Shows candles held
- Shows risk/reward
- Clearly identifies the current validation window
- Does NOT alter trading logic
- Does NOT alter optimisation
- Does NOT alter validation thresholds
"""

from __future__ import annotations

from collections import defaultdict

from data.market_data import MarketData

from indicators.composite import build_indicator_set

from optimisation.optimizer import StrategyOptimizer

from backtesting.engine import BacktestEngine

from validation.window import WindowGenerator

from validation.metrics import ValidationMetrics

from database.validation import ValidationDatabase

from research.regime_detector import RegimeDetector


class WalkForwardValidator:
    """
    Walk-forward validation engine.

    Training data is used exclusively for optimisation.

    The resulting parameters are locked.

    The locked parameters are then tested against completely
    unseen validation data.

    Validation classification:

        PASS
            Strong performance with sufficient sample.

        PASS_LOW_SAMPLE
            Strong performance but insufficient trades for
            strong statistical confidence.

        FAIL
            Performance or robustness requirements failed.

    Additional diagnostics identify:

        - strategy performance
        - direction performance
        - exit reason performance
        - winning / losing trades
        - trade duration
        - largest winner
        - largest loser
        - every individual trade
    """

    def __init__(
        self,
        symbol="SPY",
        starting_cash=100000.0,
        training_size=1000,
        validation_size=250,
        step_size=250,
        expanding=True,
        max_windows=None,
    ):

        self.symbol = symbol

        self.starting_cash = starting_cash

        self.max_windows = max_windows

        self.market = MarketData()

        self.optimizer = StrategyOptimizer(
            starting_cash=starting_cash
        )

        self.window_generator = WindowGenerator(
            training_size=training_size,
            validation_size=validation_size,
            step_size=step_size,
            expanding=expanding,
        )

        self.database = ValidationDatabase()

        self.regime_detector = RegimeDetector()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        dataframe = self.market.get_history(
            symbol=self.symbol,
            period="10y",
            interval="1d",
        )

        dataframe = build_indicator_set(
            dataframe.copy()
        )

        print()

        print(
            f"Dataset candles available: {len(dataframe)}"
        )

        return dataframe

    # =====================================================
    # TRADE DIAGNOSTICS
    # =====================================================

    def print_trade_diagnostics(
        self,
        validation_result,
        window_number=None,
    ):
        """
        Analyse the simulated trades returned by the
        BacktestEngine.

        This operates entirely on the already completed
        validation result.

        It does not alter trading logic.

        In addition to aggregate statistics, every individual
        trade is printed so failed validation windows can be
        investigated.
        """

        trades = validation_result.get(
            "trade_list",
            []
        )

        print()

        print(
            "=" * 60
        )

        if window_number is not None:

            print(
                f"TRADE DIAGNOSTICS - WINDOW {window_number}"
            )

        else:

            print(
                "TRADE DIAGNOSTICS"
            )

        print(
            "=" * 60
        )

        if not trades:

            print()

            print(
                "No trades available for diagnostics."
            )

            return

        total = len(trades)

        # =================================================
        # BASIC STATISTICS
        # =================================================

        profits = [
            float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )
            for trade in trades
        ]

        winners = [
            value
            for value in profits
            if value > 0
        ]

        losers = [
            value
            for value in profits
            if value < 0
        ]

        total_profit = sum(
            profits
        )

        average_trade = (
            total_profit / total
            if total
            else 0.0
        )

        largest_winner = (
            max(winners)
            if winners
            else 0.0
        )

        largest_loser = (
            min(losers)
            if losers
            else 0.0
        )

        print()

        print(
            f"Total trades: {total}"
        )

        print(
            f"Winning trades: "
            f"{len(winners)}"
        )

        print(
            f"Losing trades: "
            f"{len(losers)}"
        )

        print(
            f"Average trade: "
            f"{average_trade:.2f}"
        )

        print(
            f"Largest winner: "
            f"{largest_winner:.2f}"
        )

        print(
            f"Largest loser: "
            f"{largest_loser:.2f}"
        )

        # =================================================
        # DIRECTION BREAKDOWN
        # =================================================

        direction_stats = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0.0,
            }
        )

        for trade in trades:

            direction = str(
                getattr(
                    trade,
                    "direction",
                    "UNKNOWN"
                )
            ).upper()

            profit = float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )

            stats = direction_stats[
                direction
            ]

            stats["trades"] += 1

            stats["profit"] += profit

            if profit > 0:

                stats["wins"] += 1

            elif profit < 0:

                stats["losses"] += 1

        print()

        print(
            "DIRECTION BREAKDOWN"
        )

        for direction, stats in sorted(
            direction_stats.items()
        ):

            win_rate = (
                stats["wins"]
                /
                stats["trades"]
                *
                100
                if stats["trades"] > 0
                else 0.0
            )

            print(
                f"  {direction}: "
                f"{stats['trades']} trades | "
                f"Wins {stats['wins']} | "
                f"Losses {stats['losses']} | "
                f"Win Rate {win_rate:.2f}% | "
                f"Profit {stats['profit']:.2f}"
            )

        # =================================================
        # STRATEGY BREAKDOWN
        # =================================================

        strategy_stats = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0.0,
            }
        )

        for trade in trades:

            strategy = str(
                getattr(
                    trade,
                    "strategy",
                    "UNKNOWN"
                )
            )

            profit = float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )

            stats = strategy_stats[
                strategy
            ]

            stats["trades"] += 1

            stats["profit"] += profit

            if profit > 0:

                stats["wins"] += 1

            elif profit < 0:

                stats["losses"] += 1

        print()

        print(
            "STRATEGY BREAKDOWN"
        )

        for strategy, stats in sorted(
            strategy_stats.items()
        ):

            win_rate = (
                stats["wins"]
                /
                stats["trades"]
                *
                100
                if stats["trades"] > 0
                else 0.0
            )

            print(
                f"  {strategy}: "
                f"{stats['trades']} trades | "
                f"Wins {stats['wins']} | "
                f"Losses {stats['losses']} | "
                f"Win Rate {win_rate:.2f}% | "
                f"Profit {stats['profit']:.2f}"
            )

        # =================================================
        # EXIT REASON BREAKDOWN
        # =================================================

        exit_stats = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0.0,
            }
        )

        for trade in trades:

            reason = str(
                getattr(
                    trade,
                    "exit_reason",
                    "UNKNOWN"
                )
            )

            profit = float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )

            stats = exit_stats[
                reason
            ]

            stats["trades"] += 1

            stats["profit"] += profit

            if profit > 0:

                stats["wins"] += 1

            elif profit < 0:

                stats["losses"] += 1

        print()

        print(
            "EXIT REASON BREAKDOWN"
        )

        for reason, stats in sorted(
            exit_stats.items()
        ):

            win_rate = (
                stats["wins"]
                /
                stats["trades"]
                *
                100
                if stats["trades"] > 0
                else 0.0
            )

            print(
                f"  {reason}: "
                f"{stats['trades']} trades | "
                f"Wins {stats['wins']} | "
                f"Losses {stats['losses']} | "
                f"Win Rate {win_rate:.2f}% | "
                f"Profit {stats['profit']:.2f}"
            )

        # =================================================
        # HOLDING PERIOD
        # =================================================

        holding_periods = []

        for trade in trades:

            candles = int(
                getattr(
                    trade,
                    "candles_held",
                    0
                )
            )

            holding_periods.append(
                candles
            )

        if holding_periods:

            average_hold = (
                sum(
                    holding_periods
                )
                /
                len(
                    holding_periods
                )
            )

            longest_hold = max(
                holding_periods
            )

            shortest_hold = min(
                holding_periods
            )

            print()

            print(
                "HOLDING PERIOD"
            )

            print(
                f"  Average: "
                f"{average_hold:.2f} candles"
            )

            print(
                f"  Shortest: "
                f"{shortest_hold} candles"
            )

            print(
                f"  Longest: "
                f"{longest_hold} candles"
            )

        # =================================================
        # RISK / REWARD
        # =================================================

        risk_rewards = []

        for trade in trades:

            rr = float(
                getattr(
                    trade,
                    "risk_reward",
                    0.0
                )
            )

            if rr > 0:

                risk_rewards.append(
                    rr
                )

        if risk_rewards:

            average_rr = (
                sum(
                    risk_rewards
                )
                /
                len(
                    risk_rewards
                )
            )

            print()

            print(
                "RISK / REWARD"
            )

            print(
                f"  Average R:R: "
                f"{average_rr:.2f}"
            )

        # =================================================
        # INDIVIDUAL TRADE REPORT
        # =================================================
        #
        # This is the important new diagnostic section.
        #
        # We deliberately print every trade in chronological
        # order rather than only the worst/best five.
        #
        # This allows us to see whether Window 2 is suffering
        # from:
        #
        # - repeated stops
        # - repeated breakeven exits
        # - poor direction selection
        # - unrealistic targets
        # - long losing holds
        # - one particular strategy failing
        #
        # =================================================

        print()

        print(
            "=" * 60
        )

        print(
            "INDIVIDUAL TRADE REPORT"
        )

        print(
            "=" * 60
        )

        for trade_number, trade in enumerate(
            trades,
            start=1
        ):

            direction = str(
                getattr(
                    trade,
                    "direction",
                    "UNKNOWN"
                )
            )

            strategy = str(
                getattr(
                    trade,
                    "strategy",
                    "UNKNOWN"
                )
            )

            exit_reason = str(
                getattr(
                    trade,
                    "exit_reason",
                    "UNKNOWN"
                )
            )

            entry = float(
                getattr(
                    trade,
                    "entry",
                    0.0
                )
            )

            exit_price = float(
                getattr(
                    trade,
                    "exit",
                    0.0
                )
            )

            profit_loss = float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )

            candles_held = int(
                getattr(
                    trade,
                    "candles_held",
                    0
                )
            )

            risk_reward = float(
                getattr(
                    trade,
                    "risk_reward",
                    0.0
                )
            )

            quantity = int(
                getattr(
                    trade,
                    "quantity",
                    0
                )
            )

            if profit_loss > 0:

                result = "WIN"

            elif profit_loss < 0:

                result = "LOSS"

            else:

                result = "BREAKEVEN"

            print()

            print(
                f"Trade {trade_number}/{total}"
            )

            print(
                f"  Result:       {result}"
            )

            print(
                f"  Direction:    {direction}"
            )

            print(
                f"  Strategy:     {strategy}"
            )

            print(
                f"  Entry:        {entry:.2f}"
            )

            print(
                f"  Exit:         {exit_price:.2f}"
            )

            print(
                f"  P/L:          {profit_loss:.2f}"
            )

            print(
                f"  Exit reason:  {exit_reason}"
            )

            print(
                f"  Candles held: {candles_held}"
            )

            print(
                f"  Quantity:     {quantity}"
            )

            print(
                f"  Risk / Reward:{risk_reward:.2f}"
            )

        # =================================================
        # WORST TRADES
        # =================================================

        sorted_trades = sorted(
            trades,
            key=lambda trade:
            float(
                getattr(
                    trade,
                    "profit_loss",
                    0.0
                )
            )
        )

        print()

        print(
            "WORST 5 TRADES"
        )

        for trade in sorted_trades[:5]:

            print(
                f"  "
                f"{getattr(trade, 'direction', 'UNKNOWN')} "
                f"| "
                f"{getattr(trade, 'strategy', 'UNKNOWN')} "
                f"| "
                f"{getattr(trade, 'exit_reason', 'UNKNOWN')} "
                f"| "
                f"P/L {float(getattr(trade, 'profit_loss', 0.0)):.2f} "
                f"| "
                f"Held {getattr(trade, 'candles_held', 0)}"
            )

        # =================================================
        # BEST TRADES
        # =================================================

        print()

        print(
            "BEST 5 TRADES"
        )

        for trade in reversed(
            sorted_trades[-5:]
        ):

            print(
                f"  "
                f"{getattr(trade, 'direction', 'UNKNOWN')} "
                f"| "
                f"{getattr(trade, 'strategy', 'UNKNOWN')} "
                f"| "
                f"{getattr(trade, 'exit_reason', 'UNKNOWN')} "
                f"| "
                f"P/L {float(getattr(trade, 'profit_loss', 0.0)):.2f} "
                f"| "
                f"Held {getattr(trade, 'candles_held', 0)}"
            )

    # =====================================================
    # REGIME DIAGNOSTICS
    # =====================================================

    def print_regime_diagnostics(
        self,
        validation_dataframe,
    ):

        print()

        print(
            "REGIME DIAGNOSTICS"
        )

        try:

            regime = (
                self.regime_detector.analyse(
                    validation_dataframe
                )
            )

            print(
                f"  Overall regime: "
                f"{regime}"
            )

        except Exception as exc:

            print(
                "  Regime analysis failed: "
                f"{type(exc).__name__}: {exc}"
            )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        dataframe = self.load_data()

        windows = self.window_generator.generate(
            dataframe
        )

        if self.max_windows:

            windows = windows[
                :self.max_windows
            ]

        print()

        print(
            f"Windows Generated: {len(windows)}"
        )

        results = []

        for number, window in enumerate(
            windows,
            start=1
        ):

            print()

            print(
                "=" * 60
            )

            print(
                f"WALK FORWARD WINDOW {number}"
            )

            print(
                "=" * 60
            )

            result = self.validate_window(
                window,
                window_number=number,
            )

            results.append(
                result
            )

            try:

                self.database.save(
                    self.symbol,
                    result
                )

            except Exception:

                pass

        self.print_final_summary(
            results
        )

        return results

    # =====================================================
    # VALIDATE WINDOW
    # =====================================================

    def validate_window(
        self,
        window,
        window_number=None,
    ):

        print()

        print(
            "Optimising training period..."
        )

        training_results = self.optimizer.optimise(
            window.training,
            self.symbol
        )

        # -------------------------------------------------
        # No optimisation results
        # -------------------------------------------------

        if not training_results:

            return {

                "symbol":
                    self.symbol,

                "verdict":
                    "FAIL",

                "reason":
                    "NO_RESULTS",

                "failure_reasons":
                    [
                        "NO_RESULTS"
                    ],

                "parameters":
                    {},

                "validation":
                    {},

                "metrics":
                    {},

                "regime":
                    {},
            }

        # -------------------------------------------------
        # Select best training configuration
        # -------------------------------------------------

        best = max(
            training_results,
            key=lambda x:
            x.get(
                "ranking_score",
                x.get(
                    "profit",
                    0
                )
            )
        )

        # -------------------------------------------------
        # Lock parameters
        # -------------------------------------------------

        parameters = {

            "score_threshold":
                best.get(
                    "score_threshold",
                    40
                ),

            "confidence":
                best.get(
                    "confidence",
                    0.40
                ),

            "atr_stop":
                best.get(
                    "atr_stop",
                    3.0
                ),

            "atr_target":
                best.get(
                    "atr_target",
                    5.0
                ),
        }

        print()

        print(
            "LOCKED PARAMETERS"
        )

        print(
            parameters
        )

        # -------------------------------------------------
        # Training configuration diagnostics
        # -------------------------------------------------

        print()

        print(
            "TRAINING WINNING CONFIGURATION"
        )

        print(
            f"  Ranking score: "
            f"{best.get('ranking_score', 0):.2f}"
        )

        print(
            f"  Training profit: "
            f"{best.get('profit', 0):.2f}"
        )

        print(
            f"  Training trades: "
            f"{best.get('trades', best.get('total_trades', 0))}"
        )

        print(
            f"  Training win rate: "
            f"{best.get('win_rate', 0):.2f}%"
        )

        print(
            f"  Training profit factor: "
            f"{best.get('profit_factor', 0):.2f}"
        )

        print(
            f"  Training max drawdown: "
            f"{best.get('max_drawdown', 0):.2f}%"
        )

        # -------------------------------------------------
        # Unseen validation
        # -------------------------------------------------

        print()

        print(
            "Testing unseen validation data..."
        )

        engine = BacktestEngine(
            starting_cash=self.starting_cash,

            minimum_score=
                parameters[
                    "score_threshold"
                ],

            minimum_confidence=
                parameters[
                    "confidence"
                ],

            atr_stop=
                parameters[
                    "atr_stop"
                ],

            atr_target=
                parameters[
                    "atr_target"
                ],
        )

        validation_result = engine.run(
            symbol=self.symbol,
            dataframe=window.validation,
        )

        # -------------------------------------------------
        # Detailed trade diagnostics
        # -------------------------------------------------

        self.print_trade_diagnostics(
            validation_result,
            window_number=window_number,
        )

        # -------------------------------------------------
        # Regime diagnostics
        # -------------------------------------------------

        self.print_regime_diagnostics(
            window.validation
        )

        # -------------------------------------------------
        # Calculate validation metrics
        # -------------------------------------------------

        metrics = ValidationMetrics.from_result(
            validation_result
        )

        robustness_score = (
            metrics.robustness_score()
        )

        # -------------------------------------------------
        # Determine classification
        # -------------------------------------------------

        verdict = metrics.classification()

        # -------------------------------------------------
        # Failure / warning reasons
        # -------------------------------------------------

        failure_reasons = (
            metrics.failure_reasons()
        )

        performance_failures = (
            metrics.performance_failure_reasons()
        )

        # -------------------------------------------------
        # Output metrics
        # -------------------------------------------------

        print()

        print(
            "=" * 60
        )

        print(
            "VALIDATION METRICS"
        )

        print(
            "=" * 60
        )

        print()

        print(
            f"Profit: "
            f"{metrics.profit:.2f}"
        )

        print(
            f"Trades: "
            f"{metrics.total_trades}"
        )

        print(
            f"Win Rate: "
            f"{metrics.win_rate:.2f}%"
        )

        print(
            f"Profit Factor: "
            f"{metrics.profit_factor:.2f}"
        )

        # -------------------------------------------------
        # Show capped PF used for scoring when necessary
        # -------------------------------------------------

        scoring_profit_factor = min(
            max(
                metrics.profit_factor,
                0.0
            ),
            4.0
        )

        if (
            metrics.profit_factor
            != scoring_profit_factor
        ):

            print(
                f"Scoring Profit Factor: "
                f"{scoring_profit_factor:.2f}"
            )

        print(
            f"Max Drawdown: "
            f"{metrics.max_drawdown:.2f}%"
        )

        print(
            f"Robustness Score: "
            f"{robustness_score:.1f}/100"
        )

        print()

        print(
            f"RESULT: {verdict}"
        )

        # -------------------------------------------------
        # Sample warning
        # -------------------------------------------------

        if not metrics.sample_is_sufficient():

            print()

            print(
                "STATISTICAL WARNING"
            )

            print(
                f"- Only {metrics.total_trades} "
                f"trades observed"
            )

            print(
                f"- Minimum recommended sample: "
                f"{metrics.MIN_SAMPLE_SIZE}"
            )

            print(
                "- Performance is promising, but "
                "statistical confidence is limited."
            )

        # -------------------------------------------------
        # Failure reasons
        # -------------------------------------------------

        if failure_reasons:

            print()

            print(
                "VALIDATION DIAGNOSTICS"
            )

            for reason in failure_reasons:

                if (
                    reason
                    == "INSUFFICIENT_SAMPLE"
                ):

                    print(
                        "- "
                        f"{reason} "
                        "(warning)"
                    )

                else:

                    print(
                        f"- {reason}"
                    )

        else:

            print()

            print(
                "NO FAILURE REASONS"
            )

        # -------------------------------------------------
        # Regime object for persistence
        # -------------------------------------------------

        try:

            regime = (
                self.regime_detector.analyse(
                    window.validation
                )
            )

        except Exception:

            regime = {}

        # -------------------------------------------------
        # Return complete result
        # -------------------------------------------------

        return {

            "symbol":
                self.symbol,

            "parameters":
                parameters,

            "training_best":
                best,

            "validation":
                validation_result,

            "metrics":
                metrics.to_dict(),

            "regime":
                regime,

            "verdict":
                verdict,

            "failure_reasons":
                failure_reasons,

            "performance_failure_reasons":
                performance_failures,

            "sample_sufficient":
                metrics.sample_is_sufficient(),

        }

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    def print_final_summary(
        self,
        results,
    ):

        print()

        print(
            "=" * 60
        )

        print(
            "FINAL SUMMARY"
        )

        print(
            "=" * 60
        )

        # -------------------------------------------------
        # Classification counts
        # -------------------------------------------------

        passed = sum(
            1
            for result in results
            if result.get(
                "verdict"
            ) == "PASS"
        )

        low_sample = sum(
            1
            for result in results
            if result.get(
                "verdict"
            ) == "PASS_LOW_SAMPLE"
        )

        failed = sum(
            1
            for result in results
            if result.get(
                "verdict"
            ) == "FAIL"
        )

        print()

        print(
            f"PASS: "
            f"{passed}/{len(results)}"
        )

        print(
            f"PASS_LOW_SAMPLE: "
            f"{low_sample}/{len(results)}"
        )

        print(
            f"FAIL: "
            f"{failed}/{len(results)}"
        )

        # -------------------------------------------------
        # Overall interpretation
        # -------------------------------------------------

        if failed == 0 and low_sample == 0:

            print()

            print(
                "OVERALL RESULT: PASS"
            )

        elif failed == 0:

            print()

            print(
                "OVERALL RESULT: "
                "PROMISING / LOW SAMPLE"
            )

        else:

            print()

            print(
                "OVERALL RESULT: FAIL"
            )

        # -------------------------------------------------
        # Window summary
        # -------------------------------------------------

        print()

        print(
            "WINDOW SUMMARY"
        )

        for number, result in enumerate(
            results,
            start=1
        ):

            metrics = result.get(
                "metrics",
                {}
            )

            verdict = result.get(
                "verdict",
                "FAIL"
            )

            reasons = result.get(
                "failure_reasons",
                []
            )

            parameters = result.get(
                "parameters",
                {}
            )

            regime = result.get(
                "regime",
                {}
            )

            print()

            print(
                f"Window {number}: "
                f"{verdict}"
            )

            print(
                f"  Locked parameters: "
                f"{parameters}"
            )

            print(
                f"  Regime: "
                f"{regime}"
            )

            print(
                f"  Profit: "
                f"{metrics.get('profit', 0):.2f}"
            )

            print(
                f"  Trades: "
                f"{metrics.get('total_trades', 0)}"
            )

            print(
                f"  Win Rate: "
                f"{metrics.get('win_rate', 0):.2f}%"
            )

            print(
                f"  Profit Factor: "
                f"{metrics.get('profit_factor', 0):.2f}"
            )

            print(
                f"  Max Drawdown: "
                f"{metrics.get('max_drawdown', 0):.2f}%"
            )

            print(
                f"  Robustness: "
                f"{metrics.get('robustness_score', 0):.1f}/100"
            )

            print(
                f"  Sample Sufficient: "
                f"{metrics.get('sample_sufficient', False)}"
            )

            if reasons:

                print(
                    "  Diagnostics: "
                    + ", ".join(
                        reasons
                    )
                )

            else:

                print(
                    "  Diagnostics: NONE"
                )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    validator = WalkForwardValidator(

        symbol="SPY",

        max_windows=6,

    )

    validator.run()