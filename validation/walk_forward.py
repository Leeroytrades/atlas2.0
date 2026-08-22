"""
Atlas AI Trading Platform 4.6

Walk Forward Validation Engine

Responsible for:

- Loading historical market data
- Creating chronological training/validation windows
- Optimising strategy parameters on training data only
- Locking the best training parameters
- Testing those parameters on completely unseen validation data
- Preventing training-data leakage
- Recording validation results
- Regime analysis
- Combined validation statistics
- Robustness scoring
- Validation reporting

IMPORTANT:

Training data is used ONLY for optimisation.

Validation data is never passed to the optimiser.

The selected parameters are locked before
validation testing begins.
"""

from __future__ import annotations

from dataclasses import dataclass


# ============================================================
# IMPORTS
# ============================================================

from data.market_data import MarketData

from optimisation.optimizer import (
    StrategyOptimizer,
)

from backtesting.engine import (
    BacktestEngine,
)

from validation.database import (
    ValidationDatabase,
)

from research.regime_detector import (
    RegimeDetector,
)


# ============================================================
# VALIDATION WINDOW
# ============================================================


@dataclass(slots=True)
class ValidationWindow:

    training: object

    validation: object

    def __str__(self):

        return (
            f"Training candles: {len(self.training)} | "
            f"Validation candles: {len(self.validation)}"
        )


# ============================================================
# WINDOW GENERATOR
# ============================================================


class WindowGenerator:

    def __init__(
        self,
        training_size: int = 500,
        validation_size: int = 250,
        step_size: int = 100,
        expanding: bool = True,
    ):

        self.training_size = int(
            training_size
        )

        self.validation_size = int(
            validation_size
        )

        self.step_size = int(
            step_size
        )

        self.expanding = bool(
            expanding
        )

    # ========================================================
    # GENERATE WINDOWS
    # ========================================================

    def generate(
        self,
        dataframe,
    ):

        windows = []

        if dataframe is None:

            print(
                "WINDOW ERROR: Dataset is None"
            )

            return windows

        total_rows = len(
            dataframe
        )

        print()

        print(
            f"Dataset candles available: "
            f"{total_rows}"
        )

        print(
            f"Training size: "
            f"{self.training_size}"
        )

        print(
            f"Validation size: "
            f"{self.validation_size}"
        )

        print(
            f"Step size: "
            f"{self.step_size}"
        )

        print(
            f"Expanding training: "
            f"{self.expanding}"
        )

        required_rows = (
            self.training_size
            +
            self.validation_size
        )

        print(
            f"Required per window: "
            f"{required_rows}"
        )

        if total_rows < required_rows:

            print()

            print(
                "WINDOW ERROR: Not enough data"
            )

            return windows

        if self.step_size <= 0:

            print()

            print(
                "WINDOW ERROR: "
                "step_size must be greater than zero"
            )

            return windows

        start = 0

        while True:

            # ------------------------------------------------
            # TRAINING WINDOW
            # ------------------------------------------------

            if self.expanding:

                training_start = 0

            else:

                training_start = start

            training_end = (
                start
                +
                self.training_size
            )

            # ------------------------------------------------
            # VALIDATION WINDOW
            # ------------------------------------------------

            validation_start = (
                training_end
            )

            validation_end = (
                training_end
                +
                self.validation_size
            )

            # ------------------------------------------------
            # Stop when validation exceeds dataset
            # ------------------------------------------------

            if validation_end > total_rows:

                break

            # ------------------------------------------------
            # Slice data
            # ------------------------------------------------

            training = dataframe.iloc[
                training_start:
                training_end
            ].copy()

            validation = dataframe.iloc[
                validation_start:
                validation_end
            ].copy()

            # ------------------------------------------------
            # Safety checks
            # ------------------------------------------------

            if len(training) < self.training_size:

                break

            if len(validation) < self.validation_size:

                break

            # ------------------------------------------------
            # Create window
            # ------------------------------------------------

            windows.append(

                ValidationWindow(

                    training=training,

                    validation=validation,

                )

            )

            # ------------------------------------------------
            # Move forward chronologically
            # ------------------------------------------------

            start += self.step_size

        print()

        print(
            f"Generated validation windows: "
            f"{len(windows)}"
        )

        return windows


# ============================================================
# VALIDATION RESULT
# ============================================================


@dataclass(slots=True)
class ValidationWindowResult:

    window_id: int

    parameters: dict

    training: dict

    validation: dict

    verdict: str

    robustness_score: float

    regime: str = "UNKNOWN"

    regime_confidence: float = 0.0


# ============================================================
# WALK FORWARD VALIDATOR
# ============================================================


class WalkForwardValidator:

    # ========================================================
    # VALIDATION RULES
    # ========================================================

    MIN_VALIDATION_TRADES = 1

    MIN_PROFIT_FACTOR = 1.0

    MIN_WIN_RATE = 30.0

    MAX_DRAWDOWN = 30.0

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        symbol="SPY",
        starting_cash=100000.0,

        training_size=500,

        validation_size=250,

        step_size=100,

        expanding=True,

        max_windows=None,
    ):

        self.symbol = symbol

        self.starting_cash = float(
            starting_cash
        )

        self.max_windows = max_windows

        # ----------------------------------------------------
        # Market data
        # ----------------------------------------------------

        self.market = MarketData()

        # ----------------------------------------------------
        # Optimiser
        # ----------------------------------------------------

        self.optimizer = StrategyOptimizer(

            starting_cash=
                self.starting_cash

        )

        # ----------------------------------------------------
        # Window generator
        # ----------------------------------------------------

        self.window_generator = WindowGenerator(

            training_size=
                training_size,

            validation_size=
                validation_size,

            step_size=
                step_size,

            expanding=
                expanding,

        )

        # ----------------------------------------------------
        # Validation database
        # ----------------------------------------------------

        self.database = ValidationDatabase()

        # ----------------------------------------------------
        # Regime detector
        # ----------------------------------------------------

        self.regime_detector = RegimeDetector()

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        self.results = []

    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(
        self,
    ):

        dataframe = None

        errors = []

        # ----------------------------------------------------
        # get_data
        # ----------------------------------------------------

        if hasattr(
            self.market,
            "get_data",
        ):

            try:

                dataframe = (
                    self.market.get_data(
                        self.symbol
                    )
                )

            except Exception as error:

                errors.append(
                    f"get_data: {error}"
                )

        # ----------------------------------------------------
        # download
        # ----------------------------------------------------

        if (
            dataframe is None
            and
            hasattr(
                self.market,
                "download",
            )
        ):

            try:

                dataframe = (
                    self.market.download(
                        self.symbol
                    )
                )

            except Exception as error:

                errors.append(
                    f"download: {error}"
                )

        # ----------------------------------------------------
        # fetch
        # ----------------------------------------------------

        if (
            dataframe is None
            and
            hasattr(
                self.market,
                "fetch",
            )
        ):

            try:

                dataframe = (
                    self.market.fetch(
                        self.symbol
                    )
                )

            except Exception as error:

                errors.append(
                    f"fetch: {error}"
                )

        # ----------------------------------------------------
        # Failure
        # ----------------------------------------------------

        if dataframe is None:

            print()

            print(
                "VALIDATION ERROR: "
                "Unable to load market data."
            )

            for error in errors:

                print(
                    f"  {error}"
                )

            return None

        # ----------------------------------------------------
        # Validate dataframe
        # ----------------------------------------------------

        if not hasattr(
            dataframe,
            "empty",
        ):

            print()

            print(
                "VALIDATION ERROR: "
                "Market data is not a dataframe."
            )

            return None

        if dataframe.empty:

            print()

            print(
                "VALIDATION ERROR: "
                "Market dataset is empty."
            )

            return None

        return dataframe

    # ========================================================
    # TRADE COUNT
    # ========================================================

    @staticmethod
    def get_trade_count(
        result: dict,
    ) -> int:

        if not isinstance(
            result,
            dict,
        ):

            return 0

        try:

            return int(
                result.get(
                    "total_trades",
                    result.get(
                        "trades",
                        result.get(
                            "trade_count",
                            0,
                        ),
                    ),
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0

    # ========================================================
    # PROFIT
    # ========================================================

    @staticmethod
    def get_profit(
        result: dict,
    ) -> float:

        if not isinstance(
            result,
            dict,
        ):

            return 0.0

        try:

            return float(
                result.get(
                    "profit",
                    result.get(
                        "net_profit",
                        0.0,
                    ),
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ========================================================
    # PROFIT FACTOR
    # ========================================================

    @staticmethod
    def get_profit_factor(
        result: dict,
    ) -> float:

        if not isinstance(
            result,
            dict,
        ):

            return 0.0

        try:

            return float(
                result.get(
                    "profit_factor",
                    0.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ========================================================
    # WIN RATE
    # ========================================================

    @staticmethod
    def get_win_rate(
        result: dict,
    ) -> float:

        if not isinstance(
            result,
            dict,
        ):

            return 0.0

        try:

            return float(
                result.get(
                    "win_rate",
                    0.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ========================================================
    # DRAWDOWN
    # ========================================================

    @staticmethod
    def get_drawdown(
        result: dict,
    ) -> float:

        if not isinstance(
            result,
            dict,
        ):

            return 0.0

        try:

            return float(
                result.get(
                    "max_drawdown",
                    0.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ========================================================
    # SELECT BEST CONFIGURATION
    # ========================================================

    def select_best_configuration(
        self,
        optimisation_results,
    ):

        if not optimisation_results:

            return None

        return self.optimizer.best(
            optimisation_results
        )

    # ========================================================
    # CREATE BACKTEST ENGINE
    # ========================================================

    def create_backtest_engine(
        self,
        parameters: dict,
    ):

        score_threshold = float(
            parameters.get(
                "score_threshold",
                40,
            )
        )

        confidence = float(
            parameters.get(
                "confidence",
                0.40,
            )
        )

        atr_stop = float(
            parameters.get(
                "atr_stop",
                2.0,
            )
        )

        atr_target = float(
            parameters.get(
                "atr_target",
                4.0,
            )
        )

        return BacktestEngine(

            starting_cash=
                self.starting_cash,

            minimum_score=
                score_threshold,

            minimum_confidence=
                confidence,

            atr_stop=
                atr_stop,

            atr_target=
                atr_target,

        )

    # ========================================================
    # RUN VALIDATION BACKTEST
    # ========================================================

    def run_validation_backtest(
        self,
        validation_dataframe,
        parameters,
    ):

        engine = self.create_backtest_engine(
            parameters
        )

        result = engine.run(

            symbol=
                self.symbol,

            dataframe=
                validation_dataframe,

        )

        if not isinstance(
            result,
            dict,
        ):

            return {

                "profit": 0.0,

                "net_profit": 0.0,

                "profit_factor": 0.0,

                "win_rate": 0.0,

                "total_trades": 0,

                "trades": 0,

                "max_drawdown": 0.0,

                "average_trade": 0.0,

                "trade_list": [],

            }

        return result

    # ========================================================
    # VERDICT
    # ========================================================

    def determine_verdict(
        self,
        validation,
    ):

        trades = self.get_trade_count(
            validation
        )

        profit = self.get_profit(
            validation
        )

        profit_factor = (
            self.get_profit_factor(
                validation
            )
        )

        win_rate = self.get_win_rate(
            validation
        )

        drawdown = self.get_drawdown(
            validation
        )

        if trades < self.MIN_VALIDATION_TRADES:

            return "FAIL"

        if profit <= 0:

            return "FAIL"

        if profit_factor < self.MIN_PROFIT_FACTOR:

            return "FAIL"

        if win_rate < self.MIN_WIN_RATE:

            return "FAIL"

        if drawdown > self.MAX_DRAWDOWN:

            return "FAIL"

        return "PASS"

    # ========================================================
    # ROBUSTNESS SCORE
    # ========================================================

    def calculate_robustness_score(
        self,
        training,
        validation,
    ):

        training_profit = self.get_profit(
            training
        )

        validation_profit = self.get_profit(
            validation
        )

        training_pf = (
            self.get_profit_factor(
                training
            )
        )

        validation_pf = (
            self.get_profit_factor(
                validation
            )
        )

        training_win_rate = (
            self.get_win_rate(
                training
            )
        )

        validation_win_rate = (
            self.get_win_rate(
                validation
            )
        )

        validation_drawdown = (
            self.get_drawdown(
                validation
            )
        )

        score = 0.0

        # ----------------------------------------------------
        # Validation profit
        # ----------------------------------------------------

        if validation_profit > 0:

            score += 30

        elif validation_profit == 0:

            score += 10

        # ----------------------------------------------------
        # Profit factor
        # ----------------------------------------------------

        if validation_pf >= 2.0:

            score += 25

        elif validation_pf >= 1.5:

            score += 20

        elif validation_pf >= 1.2:

            score += 15

        elif validation_pf >= 1.0:

            score += 10

        # ----------------------------------------------------
        # Win rate
        # ----------------------------------------------------

        if validation_win_rate >= 60:

            score += 15

        elif validation_win_rate >= 50:

            score += 12

        elif validation_win_rate >= 40:

            score += 8

        elif validation_win_rate >= 30:

            score += 4

        # ----------------------------------------------------
        # Drawdown
        # ----------------------------------------------------

        if validation_drawdown <= 5:

            score += 15

        elif validation_drawdown <= 10:

            score += 12

        elif validation_drawdown <= 20:

            score += 8

        elif validation_drawdown <= 30:

            score += 4

        # ----------------------------------------------------
        # Profit consistency
        # ----------------------------------------------------

        if training_profit > 0:

            if validation_profit > 0:

                score += 10

            else:

                score -= 10

        # ----------------------------------------------------
        # Profit factor consistency
        # ----------------------------------------------------

        if (
            training_pf > 0
            and validation_pf > 0
        ):

            ratio = (
                validation_pf
                /
                training_pf
            )

            if ratio >= 0.75:

                score += 5

            elif ratio >= 0.50:

                score += 2

            else:

                score -= 5

        # ----------------------------------------------------
        # Win-rate consistency
        # ----------------------------------------------------

        win_rate_difference = abs(
            training_win_rate
            -
            validation_win_rate
        )

        if win_rate_difference <= 10:

            score += 5

        elif win_rate_difference <= 20:

            score += 2

        else:

            score -= 5

        return round(
            max(
                0.0,
                min(
                    100.0,
                    score,
                ),
            ),
            2,
        )

    # ========================================================
    # REGIME ANALYSIS
    # ========================================================

    def analyse_regime(
        self,
        dataframe,
    ):

        try:

            result = (
                self.regime_detector.analyse(
                    dataframe
                )
            )

        except Exception:

            return (
                "UNKNOWN",
                0.0,
            )

        if isinstance(
            result,
            dict,
        ):

            regime = result.get(
                "regime",
                "UNKNOWN",
            )

            confidence = result.get(
                "confidence",
                0.0,
            )

        else:

            regime = result

            confidence = 0.0

        if not regime:

            regime = "UNKNOWN"

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError,
        ):

            confidence = 0.0

        return (
            str(regime),
            confidence,
        )

    # ========================================================
    # SAVE RESULT
    # ========================================================

    def save_result(
        self,
        result: ValidationWindowResult,
    ):

        payload = {

            "window_id":
                result.window_id,

            "training":
                result.training,

            "validation":
                result.validation,

            "parameters":
                result.parameters,

            "verdict":
                result.verdict,

        }

        try:

            self.database.save(

                self.symbol,

                payload,

            )

        except Exception as error:

            print()

            print(
                "WARNING: Unable to save "
                "validation result:"
            )

            print(
                f"  {type(error).__name__}: "
                f"{error}"
            )

    # ========================================================
    # PROCESS WINDOW
    # ========================================================

    def process_window(
        self,
        window,
        window_id: int,
    ):

        print()

        print(
            "===================================================="
        )

        print(
            f"WALK-FORWARD WINDOW {window_id}"
        )

        print(
            "===================================================="
        )

        print(
            f"Training candles: "
            f"{len(window.training)}"
        )

        print(
            f"Validation candles: "
            f"{len(window.validation)}"
        )

        # ====================================================
        # TRAINING
        # ====================================================

        print()

        print(
            "Optimising TRAINING data..."
        )

        optimisation_results = (
            self.optimizer.optimise(

                dataset=
                    window.training,

                symbol=
                    self.symbol,

            )
        )

        if not optimisation_results:

            print()

            print(
                "WINDOW FAILED: "
                "No optimisation results."
            )

            return None

        # ====================================================
        # SELECT BEST
        # ====================================================

        best = (
            self.select_best_configuration(
                optimisation_results
            )
        )

        if best is None:

            print()

            print(
                "WINDOW FAILED: "
                "No valid training configuration."
            )

            return None

        # ====================================================
        # LOCK PARAMETERS
        # ====================================================

        parameters = {

            "score_threshold":
                best.get(
                    "score_threshold",
                    40,
                ),

            "confidence":
                best.get(
                    "confidence",
                    0.40,
                ),

            "atr_stop":
                best.get(
                    "atr_stop",
                    2.0,
                ),

            "atr_target":
                best.get(
                    "atr_target",
                    4.0,
                ),

        }

        print()

        print(
            "LOCKED PARAMETERS"
        )

        print(
            f"Score threshold: "
            f"{parameters['score_threshold']}"
        )

        print(
            f"Confidence: "
            f"{parameters['confidence']}"
        )

        print(
            f"ATR stop: "
            f"{parameters['atr_stop']}"
        )

        print(
            f"ATR target: "
            f"{parameters['atr_target']}"
        )

        # ====================================================
        # TRAINING RESULT
        # ====================================================

        training_result = best.get(
            "result"
        )

        if not isinstance(
            training_result,
            dict,
        ):

            training_result = best

        # ====================================================
        # UNSEEN VALIDATION
        # ====================================================

        print()

        print(
            "Testing unseen VALIDATION data..."
        )

        validation_result = (
            self.run_validation_backtest(

                validation_dataframe=
                    window.validation,

                parameters=
                    parameters,

            )
        )

        # ====================================================
        # REGIME
        # ====================================================

        regime, regime_confidence = (
            self.analyse_regime(
                window.validation
            )
        )

        # ====================================================
        # VERDICT
        # ====================================================

        verdict = self.determine_verdict(
            validation_result
        )

        # ====================================================
        # ROBUSTNESS
        # ====================================================

        robustness_score = (
            self.calculate_robustness_score(

                training=
                    training_result,

                validation=
                    validation_result,

            )
        )

        # ====================================================
        # RESULT
        # ====================================================

        result = ValidationWindowResult(

            window_id=
                window_id,

            parameters=
                parameters,

            training=
                training_result,

            validation=
                validation_result,

            verdict=
                verdict,

            robustness_score=
                robustness_score,

            regime=
                regime,

            regime_confidence=
                regime_confidence,

        )

        self.results.append(
            result
        )

        self.save_result(
            result
        )

        # ====================================================
        # REPORT WINDOW
        # ====================================================

        print()

        print(
            "VALIDATION RESULT"
        )

        print(
            f"Profit: "
            f"{self.get_profit(validation_result):.2f}"
        )

        print(
            f"Trades: "
            f"{self.get_trade_count(validation_result)}"
        )

        print(
            f"Win rate: "
            f"{self.get_win_rate(validation_result):.2f}%"
        )

        print(
            f"Profit factor: "
            f"{self.get_profit_factor(validation_result):.2f}"
        )

        print(
            f"Max drawdown: "
            f"{self.get_drawdown(validation_result):.2f}%"
        )

        print(
            f"Regime: {regime}"
        )

        print(
            f"Regime confidence: "
            f"{regime_confidence:.2f}"
        )

        print(
            f"Robustness score: "
            f"{robustness_score:.2f}/100"
        )

        print(
            f"VERDICT: {verdict}"
        )

        return result

    # ========================================================
    # COMBINED VALIDATION PERFORMANCE
    # ========================================================

    def combined_validation_performance(
        self,
    ):

        validation_results = [
            result.validation
            for result in self.results
        ]

        total_trades = sum(
            self.get_trade_count(
                result
            )
            for result in validation_results
        )

        total_profit = sum(
            self.get_profit(
                result
            )
            for result in validation_results
        )

        wins = 0
        losses = 0

        gross_profit = 0.0
        gross_loss = 0.0

        for result in validation_results:

            trades = result.get(
                "trade_list",
                [],
            )

            if not isinstance(
                trades,
                list,
            ):

                continue

            for trade in trades:

                try:

                    if isinstance(
                        trade,
                        dict,
                    ):

                        pnl = float(
                            trade.get(
                                "profit_loss",
                                trade.get(
                                    "pnl",
                                    0,
                                ),
                            )
                        )

                    else:

                        pnl = float(
                            getattr(
                                trade,
                                "profit_loss",
                                0,
                            )
                        )

                except (
                    TypeError,
                    ValueError,
                ):

                    continue

                if pnl > 0:

                    wins += 1

                    gross_profit += pnl

                elif pnl < 0:

                    losses += 1

                    gross_loss += abs(
                        pnl
                    )

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        if (
            wins + losses == 0
            and total_trades > 0
        ):

            rates = [

                self.get_win_rate(
                    result
                )

                for result in validation_results

            ]

            if rates:

                average_win_rate = (
                    sum(rates)
                    /
                    len(rates)
                )

            else:

                average_win_rate = 0.0

            wins = round(
                total_trades
                *
                average_win_rate
                /
                100.0
            )

            losses = (
                total_trades
                -
                wins
            )

        # ----------------------------------------------------
        # Profit factor
        # ----------------------------------------------------

        if gross_loss > 0:

            profit_factor = (
                gross_profit
                /
                gross_loss
            )

        else:

            profit_factor = 0.0

        # ----------------------------------------------------
        # Win rate
        # ----------------------------------------------------

        if total_trades > 0:

            win_rate = (
                wins
                /
                total_trades
                *
                100.0
            )

        else:

            win_rate = 0.0

        # ----------------------------------------------------
        # Average trade
        # ----------------------------------------------------

        if total_trades > 0:

            average_trade = (
                total_profit
                /
                total_trades
            )

        else:

            average_trade = 0.0

        # ----------------------------------------------------
        # Drawdown
        # ----------------------------------------------------

        drawdowns = [

            self.get_drawdown(
                result
            )

            for result in validation_results

        ]

        max_drawdown = (
            max(drawdowns)
            if drawdowns
            else 0.0
        )

        return {

            "profit":
                round(
                    total_profit,
                    2,
                ),

            "net_profit":
                round(
                    total_profit,
                    2,
                ),

            "total_trades":
                total_trades,

            "trades":
                total_trades,

            "wins":
                wins,

            "losses":
                losses,

            "win_rate":
                round(
                    win_rate,
                    2,
                ),

            "profit_factor":
                round(
                    profit_factor,
                    2,
                ),

            "average_trade":
                round(
                    average_trade,
                    2,
                ),

            "max_drawdown":
                round(
                    max_drawdown,
                    2,
                ),

        }

    # ========================================================
    # FINAL REPORT
    # ========================================================

    def report(
        self,
    ):

        total_windows = len(
            self.results
        )

        passed = sum(

            1

            for result in self.results

            if result.verdict == "PASS"

        )

        failed = (
            total_windows
            -
            passed
        )

        if total_windows > 0:

            pass_rate = (
                passed
                /
                total_windows
                *
                100.0
            )

        else:

            pass_rate = 0.0

        combined = (
            self.combined_validation_performance()
        )

        if self.results:

            robustness = (
                sum(
                    result.robustness_score
                    for result in self.results
                )
                /
                len(
                    self.results
                )
            )

        else:

            robustness = 0.0

        print()

        print(
            "===================================================="
        )

        print(
            "FINAL WALK FORWARD REPORT"
        )

        print(
            "===================================================="
        )

        print()

        print(
            f"Total Windows: {total_windows}"
        )

        print(
            f"Passed: {passed}"
        )

        print(
            f"Failed: {failed}"
        )

        print(
            f"Pass Rate: {pass_rate:.1f}%"
        )

        print()

        print(
            "COMBINED VALIDATION PERFORMANCE"
        )

        print(
            f"Profit: "
            f"{combined['profit']:.2f}"
        )

        print(
            f"Trades: "
            f"{combined['total_trades']}"
        )

        print(
            f"Win Rate: "
            f"{combined['win_rate']:.2f}%"
        )

        print(
            f"Profit Factor: "
            f"{combined['profit_factor']:.2f}"
        )

        print(
            f"Average Trade: "
            f"{combined['average_trade']:.2f}"
        )

        print(
            f"Maximum Window Drawdown: "
            f"{combined['max_drawdown']:.2f}%"
        )

        print()

        print(
            f"Robustness Score: "
            f"{robustness:.1f}/100"
        )

        # ----------------------------------------------------
        # Regimes
        # ----------------------------------------------------

        regime_counts = {}

        for result in self.results:

            regime = result.regime

            regime_counts[regime] = (
                regime_counts.get(
                    regime,
                    0,
                )
                + 1
            )

        if regime_counts:

            print()

            print(
                "REGIME ANALYSIS"
            )

            for regime, count in (
                regime_counts.items()
            ):

                regime_results = [

                    result

                    for result in self.results

                    if result.regime == regime

                ]

                regime_passes = sum(

                    1

                    for result in regime_results

                    if result.verdict == "PASS"

                )

                print(
                    f"{regime}: "
                    f"{count} windows | "
                    f"{regime_passes} passes"
                )

        print()

        print(
            "===================================================="
        )

        return {

            "total_windows":
                total_windows,

            "passed":
                passed,

            "failed":
                failed,

            "pass_rate":
                round(
                    pass_rate,
                    2,
                ),

            "combined":
                combined,

            "robustness_score":
                round(
                    robustness,
                    2,
                ),

            "regimes":
                regime_counts,

            "results":
                self.results,

        }

    # ========================================================
    # RUN
    # ========================================================

    def run(
        self,
        dataframe=None,
    ):

        print()

        print(
            "===================================================="
        )

        print(
            "ATLAS 4.6 WALK FORWARD VALIDATION"
        )

        print(
            "===================================================="
        )

        print()

        print(
            f"Symbol: {self.symbol}"
        )

        print(
            f"Starting cash: "
            f"{self.starting_cash:.2f}"
        )

        # ====================================================
        # DATA
        # ====================================================

        if dataframe is None:

            dataframe = self.load_data()

        if dataframe is None:

            return None

        # ====================================================
        # WINDOWS
        # ====================================================

        windows = (
            self.window_generator.generate(
                dataframe
            )
        )

        if not windows:

            print()

            print(
                "WALK-FORWARD ABORTED: "
                "No validation windows generated."
            )

            return None

        # ====================================================
        # LIMIT
        # ====================================================

        if self.max_windows is not None:

            try:

                limit = int(
                    self.max_windows
                )

            except (
                TypeError,
                ValueError,
            ):

                limit = 0

            if limit > 0:

                windows = windows[
                    :limit
                ]

        # ====================================================
        # PROCESS
        # ====================================================

        print()

        print(
            f"Windows to validate: "
            f"{len(windows)}"
        )

        for window_number, window in enumerate(
            windows,
            start=1,
        ):

            try:

                result = self.process_window(

                    window=
                        window,

                    window_id=
                        window_number,

                )

                if result is None:

                    print()

                    print(
                        f"Window "
                        f"{window_number} "
                        f"could not be completed."
                    )

            except Exception as error:

                print()

                print(
                    f"Window "
                    f"{window_number} "
                    f"ERROR: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                continue

        # ====================================================
        # REPORT
        # ====================================================

        return self.report()


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":

    validator = WalkForwardValidator(

        symbol="SPY",

        starting_cash=100000.0,

        # ----------------------------------------------------
        # Atlas 4.6 whitepaper settings
        # ----------------------------------------------------

        training_size=500,

        validation_size=250,

        step_size=100,

        expanding=True,

        # ----------------------------------------------------
        # None = every generated window
        # ----------------------------------------------------

        max_windows=None,

    )

    validator.run()