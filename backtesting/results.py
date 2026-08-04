"""
Atlas AI Trading Platform 3.4

Backtesting Result Models

Centralised result objects used by:

- Backtesting
- Optimisation
- Validation
- Research reporting
"""

from __future__ import annotations


from dataclasses import dataclass, field

from typing import Any



# =====================================================
# SIMULATED TRADE RESULT
# =====================================================

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



# =====================================================
# PERFORMANCE METRICS
# =====================================================

@dataclass(slots=True)
class PerformanceMetrics:


    starting_cash: float = 0.0

    ending_equity: float = 0.0

    net_profit: float = 0.0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    profit_factor: float = 0.0

    average_trade: float = 0.0

    max_drawdown: float = 0.0



    def to_dict(
        self,
    ) -> dict:


        return {


            "starting_cash":

                self.starting_cash,


            "ending_equity":

                self.ending_equity,


            "net_profit":

                self.net_profit,


            "profit":

                self.net_profit,


            "total_trades":

                self.total_trades,


            "trades":

                self.total_trades,


            "winning_trades":

                self.winning_trades,


            "wins":

                self.winning_trades,


            "losing_trades":

                self.losing_trades,


            "losses":

                self.losing_trades,


            "win_rate":

                self.win_rate,


            "profit_factor":

                self.profit_factor,


            "average_trade":

                self.average_trade,


            "max_drawdown":

                self.max_drawdown,


        }



# =====================================================
# COMPLETE BACKTEST RESULT
# =====================================================

@dataclass
class BacktestResult:


    metrics: PerformanceMetrics = field(

        default_factory=PerformanceMetrics

    )


    trades: list[SimulatedTrade] = field(

        default_factory=list

    )


    equity_curve: list[float] = field(

        default_factory=list

    )


    metadata: dict[str, Any] = field(

        default_factory=dict

    )



    # -------------------------------------------------
    # Dictionary compatibility
    # -------------------------------------------------

    def __getitem__(

        self,

        key: str,

    ):


        return self.to_dict()[key]



    def __setitem__(

        self,

        key: str,

        value,

    ):


        self.metadata[key] = value



    def get(

        self,

        key: str,

        default=None,

    ):


        return self.to_dict().get(

            key,

            default

        )



    def update(

        self,

        values: dict,

    ):


        self.metadata.update(

            values

        )



    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def to_dict(

        self,

    ) -> dict:


        output = self.metrics.to_dict()



        output.update(

            {


                "trades":

                    [

                        {


                            "symbol":

                                trade.symbol,


                            "direction":

                                trade.direction,


                            "entry":

                                trade.entry,


                            "exit":

                                trade.exit,


                            "quantity":

                                trade.quantity,


                            "profit_loss":

                                trade.profit_loss,


                            "result":

                                trade.result,


                            "candles_held":

                                trade.candles_held,


                            "entry_index":

                                trade.entry_index,


                            "exit_index":

                                trade.exit_index,


                        }


                        for trade in self.trades

                    ],



                "equity_curve":

                    self.equity_curve,


            }

        )



        output.update(

            self.metadata

        )



        return output



    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    @property
    def profit(

        self,

    ):


        return self.metrics.net_profit



    @property
    def total_trades(

        self,

    ):


        return self.metrics.total_trades



    @property
    def win_rate(

        self,

    ):


        return self.metrics.win_rate



    @property
    def profit_factor(

        self,

    ):


        return self.metrics.profit_factor



    @property
    def max_drawdown(

        self,

    ):


        return self.metrics.max_drawdown