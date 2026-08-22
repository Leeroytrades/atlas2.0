"""
Atlas AI Trading Platform 4.4

Backtesting Trade Simulator

Canonical trade lifecycle engine used by BacktestEngine.

Responsibilities:

- Long trades
- Short trades
- ATR stops
- ATR targets
- Breakeven protection
- Maximum holding period
- Commission
- Slippage
- Strategy attribution
- Exit reason tracking
- Equity tracking
- Drawdown calculation

Execution rules:

1. Entry is already determined by BacktestEngine.

2. ATR is taken from the exact entry candle.

3. Stop/target distances use the locked ATR parameters.

4. Trade stop/target values are synchronised with the same
   ATR calculation used by the simulator.

5. If stop and target are touched on the same candle,
   STOP wins.

6. A candle that activates breakeven cannot also trigger
   the breakeven exit.

7. Maximum holding period is measured in completed candles
   after entry.

8. Only realised P/L is added to the equity curve.

9. Exit slippage is applied once.

10. Commission is applied once per completed trade.
"""

from __future__ import annotations

from dataclasses import dataclass

from models.trade import Trade


# ============================================================
# SIMULATED TRADE
# ============================================================


@dataclass(slots=True)
class SimulatedTrade:

    symbol: str

    direction: str

    entry: float

    exit: float

    quantity: int

    profit_loss: float

    result: str

    candles_held: int

    entry_index: int = 0

    exit_index: int = 0

    strategy: str = "UNKNOWN"

    exit_reason: str = "UNKNOWN"

    risk_reward: float = 0.0


# ============================================================
# SIMULATOR
# ============================================================


class Simulator:

    def __init__(
        self,
        starting_cash: float = 100000.0,
        commission: float = 1.0,
        slippage: float = 0.01,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
        max_hold: int = 100,
        breakeven_atr: float = 1.5,
    ):

        self.starting_cash = float(starting_cash)

        self.cash = float(starting_cash)

        self.commission = max(
            0.0,
            float(commission),
        )

        self.slippage = max(
            0.0,
            float(slippage),
        )

        self.atr_stop = max(
            0.0,
            float(atr_stop),
        )

        self.atr_target = max(
            0.0,
            float(atr_target),
        )

        self.max_hold = max(
            1,
            int(max_hold),
        )

        self.breakeven_atr = max(
            0.0,
            float(breakeven_atr),
        )

        self.trades: list[SimulatedTrade] = []

        self.equity_curve = [
            self.starting_cash
        ]

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.cash = float(
            self.starting_cash
        )

        self.trades = []

        self.equity_curve = [
            self.starting_cash
        ]

    # ========================================================
    # ATR
    # ========================================================

    @staticmethod
    def _get_atr(
        dataframe,
        index: int,
        entry: float,
    ) -> float:
        """
        Get ATR from the exact entry candle.

        No future ATR values are used.

        Fallback:
            2% of entry price.
        """

        atr = 0.0

        if (
            dataframe is not None
            and "ATR" in dataframe.columns
            and 0 <= index < len(dataframe)
        ):

            value = dataframe["ATR"].iloc[index]

            try:
                atr = float(value)

            except (
                TypeError,
                ValueError,
            ):

                atr = 0.0

        if atr <= 0:

            atr = (
                float(entry)
                * 0.02
            )

        return atr

    # ========================================================
    # SIMULATE TRADE
    # ========================================================

    def simulate_trade(
        self,
        trade: Trade,
        dataframe,
        index: int,
    ):
        """
        Simulate one already-created trade.

        The BacktestEngine has already determined the entry.

        The first possible exit is the candle immediately
        following the entry candle.
        """

        # ====================================================
        # VALIDATION
        # ====================================================

        if dataframe is None:
            return None

        if trade is None:
            return None

        if index < 0 or index >= len(dataframe):
            return None

        try:
            entry = float(trade.entry)
        except (
            TypeError,
            ValueError,
        ):
            return None

        if entry <= 0:
            return None

        try:
            quantity = int(trade.quantity)
        except (
            TypeError,
            ValueError,
        ):
            return None

        if quantity <= 0:
            return None

        direction = str(
            trade.direction
        ).upper().strip()

        if direction not in (
            "LONG",
            "SHORT",
        ):
            return None

        # ====================================================
        # ATR FROM EXACT ENTRY CANDLE
        # ====================================================

        atr = self._get_atr(
            dataframe,
            index,
            entry,
        )

        if atr <= 0:
            return None

        # ====================================================
        # LOCKED ATR DISTANCES
        # ====================================================

        stop_distance = (
            atr
            * self.atr_stop
        )

        target_distance = (
            atr
            * self.atr_target
        )

        if (
            stop_distance <= 0
            or target_distance <= 0
        ):
            return None

        # ====================================================
        # CANONICAL PRICE LEVELS
        # ====================================================

        if direction == "LONG":

            stop_loss = (
                entry
                - stop_distance
            )

            take_profit = (
                entry
                + target_distance
            )

        else:

            stop_loss = (
                entry
                + stop_distance
            )

            take_profit = (
                entry
                - target_distance
            )

        # ====================================================
        # SYNCHRONISE TRADE
        # ====================================================

        trade.stop_loss = stop_loss

        trade.take_profit = take_profit

        actual_risk = (
            stop_distance
            * quantity
        )

        actual_reward = (
            target_distance
            * quantity
        )

        trade.risk_amount = actual_risk

        trade.reward_amount = actual_reward

        if actual_risk > 0:

            trade.risk_reward = (
                actual_reward
                / actual_risk
            )

        else:

            trade.risk_reward = 0.0

        # ====================================================
        # BREAKEVEN
        # ====================================================

        breakeven_trigger = (
            atr
            * self.breakeven_atr
        )

        breakeven_active = False

        # ====================================================
        # STATE
        # ====================================================

        exit_price = None

        exit_reason = "END_OF_DATA"

        exit_position = (
            len(dataframe) - 1
        )

        candles_held = 0

        # ====================================================
        # FUTURE CANDLES
        # ====================================================

        for future_position in range(
            index + 1,
            len(dataframe),
        ):

            candle = dataframe.iloc[
                future_position
            ]

            # ------------------------------------------------
            # OHLC VALIDATION
            # ------------------------------------------------

            try:

                high = float(
                    candle["High"]
                )

                low = float(
                    candle["Low"]
                )

                close = float(
                    candle["Close"]
                )

            except (
                TypeError,
                ValueError,
                KeyError,
            ):

                # Invalid candles are not execution candles.
                # They are also not counted toward max_hold.
                continue

            if (
                high <= 0
                or low <= 0
                or close <= 0
                or high < low
            ):

                continue

            # This candle is now a completed candle after entry.
            candles_held += 1

            # =================================================
            # LONG
            # =================================================

            if direction == "LONG":

                stop_hit = (
                    low <= stop_loss
                )

                target_hit = (
                    high >= take_profit
                )

                # ------------------------------------------------
                # STOP + TARGET
                # ------------------------------------------------

                if (
                    stop_hit
                    and target_hit
                ):

                    exit_price = stop_loss

                    exit_reason = (
                        "STOP_SAME_CANDLE"
                    )

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # TARGET
                # ------------------------------------------------

                if target_hit:

                    exit_price = take_profit

                    exit_reason = "TARGET"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # EXISTING BREAKEVEN
                # ------------------------------------------------

                if (
                    breakeven_active
                    and low <= entry
                ):

                    exit_price = entry

                    exit_reason = "BREAKEVEN"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # ORIGINAL STOP
                # ------------------------------------------------

                if stop_hit:

                    exit_price = stop_loss

                    exit_reason = "STOP"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # BREAKEVEN ACTIVATION
                #
                # Deliberately occurs after exit checks.
                # ------------------------------------------------

                if (
                    not breakeven_active
                    and breakeven_trigger > 0
                    and high >= (
                        entry
                        + breakeven_trigger
                    )
                ):

                    breakeven_active = True

            # =================================================
            # SHORT
            # =================================================

            else:

                stop_hit = (
                    high >= stop_loss
                )

                target_hit = (
                    low <= take_profit
                )

                # ------------------------------------------------
                # STOP + TARGET
                # ------------------------------------------------

                if (
                    stop_hit
                    and target_hit
                ):

                    exit_price = stop_loss

                    exit_reason = (
                        "STOP_SAME_CANDLE"
                    )

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # TARGET
                # ------------------------------------------------

                if target_hit:

                    exit_price = take_profit

                    exit_reason = "TARGET"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # EXISTING BREAKEVEN
                # ------------------------------------------------

                if (
                    breakeven_active
                    and high >= entry
                ):

                    exit_price = entry

                    exit_reason = "BREAKEVEN"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # ORIGINAL STOP
                # ------------------------------------------------

                if stop_hit:

                    exit_price = stop_loss

                    exit_reason = "STOP"

                    exit_position = (
                        future_position
                    )

                    break

                # ------------------------------------------------
                # BREAKEVEN ACTIVATION
                # ------------------------------------------------

                if (
                    not breakeven_active
                    and breakeven_trigger > 0
                    and low <= (
                        entry
                        - breakeven_trigger
                    )
                ):

                    breakeven_active = True

            # =================================================
            # MAX HOLD
            # =================================================

            if candles_held >= self.max_hold:

                exit_price = close

                exit_reason = "MAX_HOLD"

                exit_position = (
                    future_position
                )

                break

        # =====================================================
        # END OF DATA
        # =====================================================

        if exit_price is None:

            exit_price = float(
                dataframe[
                    "Close"
                ].iloc[-1]
            )

            exit_position = (
                len(dataframe) - 1
            )

            exit_reason = "END_OF_DATA"

            candles_held = max(
                candles_held,
                max(
                    0,
                    exit_position - index,
                ),
            )

        # =====================================================
        # EXIT SLIPPAGE
        #
        # Applied exactly once.
        # =====================================================

        if direction == "LONG":

            exit_price -= self.slippage

        else:

            exit_price += self.slippage

        # =====================================================
        # CLOSE TRADE
        # =====================================================

        trade.close(
            exit_price
        )

        gross_profit_loss = float(
            trade.profit_loss
        )

        # =====================================================
        # COMMISSION
        # =====================================================

        profit_loss = (
            gross_profit_loss
            - self.commission
        )

        # =====================================================
        # STRATEGY
        # =====================================================

        strategy = getattr(
            trade,
            "strategy",
            "UNKNOWN",
        )

        if not strategy:
            strategy = "UNKNOWN"

        strategy = str(
            strategy
        ).strip()

        if not strategy:
            strategy = "UNKNOWN"

        # =====================================================
        # RESULT
        # =====================================================

        if profit_loss > 0:

            result = "WIN"

        elif profit_loss < 0:

            result = "LOSS"

        else:

            result = "BREAKEVEN"

        # =====================================================
        # SIMULATED TRADE
        # =====================================================

        simulated = SimulatedTrade(

            symbol=trade.symbol,

            direction=direction,

            entry=round(
                entry,
                2,
            ),

            exit=round(
                exit_price,
                2,
            ),

            quantity=quantity,

            profit_loss=round(
                profit_loss,
                2,
            ),

            result=result,

            candles_held=candles_held,

            entry_index=index,

            exit_index=exit_position,

            strategy=strategy,

            exit_reason=exit_reason,

            risk_reward=round(
                trade.risk_reward,
                2,
            ),
        )

        # =====================================================
        # STORE
        # =====================================================

        self.trades.append(
            simulated
        )

        self.cash += profit_loss

        self.equity_curve.append(
            self.cash
        )

        return simulated

    # ========================================================
    # RESULTS
    # ========================================================

    def results(self):

        wins = [
            trade
            for trade in self.trades
            if trade.profit_loss > 0
        ]

        losses = [
            trade
            for trade in self.trades
            if trade.profit_loss < 0
        ]

        gross_profit = sum(
            trade.profit_loss
            for trade in wins
        )

        gross_loss = abs(
            sum(
                trade.profit_loss
                for trade in losses
            )
        )

        total = len(
            self.trades
        )

        if gross_loss > 0:

            profit_factor = (
                gross_profit
                / gross_loss
            )

        else:

            profit_factor = 0.0

        if total > 0:

            win_rate = (
                len(wins)
                / total
                * 100.0
            )

        else:

            win_rate = 0.0

        net_profit = (
            self.cash
            - self.starting_cash
        )

        if total > 0:

            average_trade = (
                net_profit
                / total
            )

        else:

            average_trade = 0.0

        return {

            "starting_cash": round(
                self.starting_cash,
                2,
            ),

            "ending_equity": round(
                self.cash,
                2,
            ),

            "net_profit": round(
                net_profit,
                2,
            ),

            "profit": round(
                net_profit,
                2,
            ),

            "total_trades": total,

            "trades": total,

            "wins": len(wins),

            "losses": len(losses),

            "winning_trades": len(wins),

            "losing_trades": len(losses),

            "win_rate": round(
                win_rate,
                2,
            ),

            "profit_factor": round(
                profit_factor,
                2,
            ),

            "average_trade": round(
                average_trade,
                2,
            ),

            "max_drawdown": self.calculate_drawdown(),

            "trade_list": self.trades,

            "equity_curve": self.equity_curve,
        }

    # ========================================================
    # MAX DRAWDOWN
    # ========================================================

    def calculate_drawdown(self):

        if not self.equity_curve:
            return 0.0

        peak = float(
            self.equity_curve[0]
        )

        max_drawdown = 0.0

        for value in self.equity_curve:

            value = float(value)

            if value > peak:
                peak = value

            if peak <= 0:
                continue

            drawdown = (
                (peak - value)
                / peak
                * 100.0
            )

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return round(
            max_drawdown,
            2,
        )