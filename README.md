Atlas AI Trading Platform
Version: Atlas 3.2

A modular quantitative trading research platform designed for:

Historical strategy testing
Parameter optimisation
Risk analysis
Signal generation
Future live trading integration

Atlas has evolved from a simple scanner into a research engine capable of testing trading hypotheses against historical market data.

Project Vision

Atlas aims to become a professional-grade trading research assistant capable of:

Finding statistically strong trading configurations
Testing strategies across multiple markets
Avoiding overfitting through validation
Managing risk dynamically
Producing explainable trading decisions
Eventually supporting live execution
Current Architecture
Atlas AI Trading Platform

                main.py
                   |
                   |
             Strategy Runner
                   |
                   |
          Signal Generation Engine
                   |
        +----------+----------+
        |                     |
     Indicators            Scoring
        |                     |
        +----------+----------+
                   |
             Trade Creation
                   |
             Risk Management
                   |
             Backtest Engine
                   |
             Trade Simulator
                   |
             Optimisation Engine
                   |
             Results Database
Main Components
data/

Handles market data collection.

Responsibilities:

Download historical prices
Provide OHLCV datasets
Interface with external data sources
indicators/

Responsible for technical indicator generation.

Current indicators include:

EMA
SMA
RSI
MACD
Stochastic
ATR
ADX
DI+
DI-
OBV
CMF
VWAP

Indicators are generated through:

indicators/composite.py
Signal Engine

Location:

strategy/signal_generator.py

Purpose:

Creates trading decisions from market conditions.

Current filters:

Trend confirmation
Momentum confirmation
Volatility confirmation
Volume confirmation
EMA20 pullback filter

Signals:

BUY
SELL
HOLD

Supports optimiser-controlled:

Score thresholds
Confidence thresholds
Scoring System

Location:

scoring/

Modules:

trend_score.py
momentum_score.py
volatility_score.py
volume_score.py

The scorecard combines:

Trend
+
Momentum
+
Volatility
+
Volume
=
Total Score
Backtesting Engine

Location:

backtesting/

Components:

Backtest Engine

Responsible for:

Running historical tests
Applying configurations
Creating trades
Managing lifecycle
Strategy Runner

Responsible for:

Walking through historical candles
Generating signals
Applying score filters
Simulator

Responsible for:

ATR stop losses
ATR targets
Breakeven protection
Holding periods
Commission
Slippage
Equity tracking
Dataset Cache

Location:

research/dataset_cache.py

Purpose:

Avoid repeated downloads and indicator calculations.

Workflow:

Market Data

     |

Indicators

     |

Parquet Cache

     |

Optimisation
Optimisation Engine

Location:

optimisation/

Current features:

Parallel processing
Configuration testing
Result ranking
SQLite storage
Risk adjusted scoring

Current optimisation variables:

Score Threshold

Confidence Threshold

ATR Stop

ATR Target
Current Optimisation Results
SPY

Best configuration:

Score:
40

Confidence:
0.4

ATR Stop:
4.25

ATR Target:
5.0

Results:

Profit:
$184112.72

Win Rate:
32.99%

Profit Factor:
2.37
QQQ

Best configuration:

Score:
40

Confidence:
0.4

ATR Stop:
4.0

ATR Target:
5.5

Results:

Profit:
$185056.99

Win Rate:
40.81%

Profit Factor:
3.89
Important Discovery

Across multiple symbols Atlas is finding similar parameter regions:

Score:
40-50

Confidence:
0.4-0.5

ATR Stop:
3.75-4.25

ATR Target:
5.0-5.5

This suggests the strategy is finding a stable behaviour pattern rather than a single overfit solution.

Current Development Stage

Atlas is currently moving from:

Optimisation

into:

Validation

The next major feature is:

Walk Forward Testing

Planned:

Historical Data

        |

Training Period

        |

Optimisation

        |

Locked Parameters

        |

Unseen Validation

        |

Forward Test
Future Roadmap
Phase 1 - Validation
Walk forward testing
Monte Carlo trade analysis
Multi-symbol validation
Drawdown analysis
Phase 2 - Intelligence
AI signal explanations
Trade journaling
Market regime detection
Confidence calibration
Phase 3 - Live Trading
Real-time monitoring
Alerts
Broker integration
Automated execution
Development Rules

When modifying Atlas:

Preserve existing working behaviour
Optimise speed without changing results
Validate before adding complexity
Prefer modular components
Keep research reproducible
Current Status

Atlas 3.2 is stable and ready for validation development.