# Atlas AI Trading Platform

## Overview

Atlas is a modular AI-assisted trading research platform built in Python.

The goal of Atlas is not to blindly automate trading, but to create a complete research environment capable of:

* Market data ingestion
* Technical analysis
* Multi-factor scoring
* Strategy generation
* Risk management
* Backtesting
* Optimisation
* Walk-forward validation
* Regime-aware strategy selection
* Trade simulation
* Performance analysis

Atlas has evolved from a simple signal scanner into a full quantitative research framework.

Current version:

**Atlas AI Trading Platform 3.5**

---

# Core Philosophy

Atlas is built around the idea that robust trading systems should be:

* Data driven
* Tested on unseen data
* Resistant to overfitting
* Modular
* Explainable
* Adaptable to different market conditions

A strategy is not considered successful because it performs well historically.

It must survive:

1. Training optimisation
2. Parameter locking
3. Walk-forward validation
4. Multiple market regimes

---

# Technology Stack

## Language

Python 3.12

## Environment

Windows 11

Virtual environment:

```
.venv
```

## Main Libraries

* pandas
* numpy
* yfinance
* ta
* rich
* pytest

---

# Running Atlas

Activate environment:

```
.venv\Scripts\activate
```

Run main application:

```
python main.py
```

Run walk-forward validation:

```
python -m validation.walk_forward
```

---

# Current System Flow

```
Market Data
     |
     v
HistoricalData
     |
     v
Indicator Engine
     |
     v
Strategy System
     |
     v
Signal Generation
     |
     v
Risk Management
     |
     v
Trade Simulation
     |
     v
Performance Metrics
```

Research workflow:

```
Historical Data

      |

Training Window

      |

Optimisation

      |

Best Parameters Locked

      |

Unseen Validation

      |

Walk Forward Report

      |

Robustness Decision
```

---

# Completed Features

## Market Data

Completed:

* Historical price loading
* Cached datasets
* Multi-symbol support

Current default:

```
SPY
10 years
Daily candles
```

---

## Indicators

Implemented:

### Trend

* EMA 20
* EMA 50
* EMA 200
* SMA
* ADX

### Momentum

* RSI
* MACD
* MACD Signal
* MACD Histogram
* Stochastic

### Volatility

* ATR
* Bollinger Bands
* BB Width

### Volume

* OBV
* CMF
* VWAP

---

# Strategy System

Current strategies:

## Trend Strategy

Uses:

* EMA relationship
* MACD
* RSI
* Volume confirmation

Outputs:

* BUY
* SELL
* HOLD

---

## Range Strategy

Uses:

* Bollinger Bands
* RSI extremes
* Volatility confirmation

Designed for:

* Sideways markets
* Mean reversion

---

# Optimisation System

Atlas supports:

* Parameter grids
* Parallel execution
* Multiprocessing optimisation

Current optimised parameters:

Example:

```
score_threshold = 40
confidence = 0.4
atr_stop = 4.0
atr_target = 6.0
```

---

# Walk Forward Validation

The validation system:

1. Splits historical data into windows

Example:

```
Training:
1000 candles

Validation:
250 candles
```

2. Optimises training period

3. Locks parameters

4. Tests unseen validation period

5. Scores robustness

---

# Latest Successful Validation

Latest result:

```
Pass Rate: 80%

Windows:
5

Passed:
4

Failed:
1
```

Combined validation:

```
Profit:
209286.64

Trades:
181

Win Rate:
67.4%

Profit Factor:
27.34

Robustness Score:
92/100
```

---

# Important Development Rule

When modifying Atlas:

Prefer:

* Full file replacements
* Complete modules
* Clear version progression

Avoid:

* Small patches
* Hidden assumptions
* Breaking architecture

---

# Future Goals

## Phase 1

Complete strategy routing.

## Phase 2

Improve regime detection.

## Phase 3

Multiple strategies per market condition.

## Phase 4

Live market monitoring.

## Phase 5

AI explanations for every trade decision.

---

Atlas is currently a working quantitative research platform entering the strategy intelligence phase.
# Atlas AI Trading Platform Architecture

## System Overview

Atlas follows a modular architecture.

Major layers:

```
                 Atlas Engine

                      |

 ------------------------------------------------

 Data Layer

 Indicator Layer

 Strategy Layer

 Risk Layer

 Backtesting Layer

 Optimisation Layer

 Validation Layer

 Reporting Layer

 ------------------------------------------------
```

---

# Directory Structure

```
Atlas/

├── atlas/
│
│   ├── engine.py
│   ├── session.py
│   ├── watchlist.py
│   └── portfolio.py
│

├── data/
│
│   └── market_data.py
│

├── indicators/
│
│   ├── trend.py
│   ├── momentum.py
│   ├── volatility.py
│   ├── volume.py
│   └── composite.py
│

├── strategy/
│
│   ├── signal_generator.py
│   ├── trend_strategy.py
│   ├── range_strategy.py
│   ├── volatility_strategy.py
│   └── regime_filter.py
│

├── risk/
│
│   ├── risk_manager.py
│   └── trade.py
│

├── backtesting/
│
│   ├── engine.py
│   ├── simulator.py
│   ├── historical_data.py
│   └── strategy_runner.py
│

├── optimisation/
│
│   ├── optimizer.py
│   └── parallel_runner.py
│

├── validation/
│
│   ├── walk_forward.py
│   ├── window.py
│   ├── metrics.py
│   └── report.py
│

├── research/
│
│   └── regime_detector.py
│

└── database/

    └── validation.py
```

---

# Component Responsibilities

## Atlas Engine

Main application controller.

Responsible for:

* Starting sessions
* Running scans
* Connecting modules

---

# Data Layer

Responsible for:

* Downloading data
* Formatting candles
* Historical storage

Output:

Pandas DataFrame

---

# Indicator Engine

Transforms raw OHLCV data into analytical features.

Example:

Input:

```
Open
High
Low
Close
Volume
```

Output:

```
EMA_20
RSI
MACD
ATR
BB_WIDTH
```

---

# Strategy Layer

Strategies analyse indicators.

Each strategy returns:

```
{
 signal,
 score,
 confidence,
 strategy
}
```

Example:

```
BUY
score: 65
confidence: 0.65
```

---

# Regime Detection

Purpose:

Identify market environment.

Current classifications:

```
TREND

RANGE
```

Based on:

* Trend strength
* Volatility
* Momentum

---

# Backtesting Engine

Responsible for:

* Running historical simulations
* Applying parameters
* Creating trades
* Measuring results

Supports:

* Long trades
* Short trades
* ATR stops
* ATR targets

---

# Optimisation Layer

Tests parameter combinations.

Example:

```
score threshold

confidence

ATR stop

ATR target
```

Uses multiprocessing.

Current optimisation sizes:

300-700+ configurations.

---

# Validation Layer

The most important robustness component.

Flow:

```
Training Data

↓

Optimisation

↓

Best Parameters

↓

Validation Data

↓

PASS / FAIL
```

A strategy must prove itself on unseen data.

---

# Current Weaknesses

## Strategy Routing

Router exists but needs completion.

Current:

```
TREND -> TrendStrategy

RANGE -> RangeStrategy
```

Needs:

* Volatility strategy
* Dynamic switching
* Better regime confidence

---

## Validation

Current system:

Strong in trending markets.

Weak area:

Sideways normal volatility.

---

# Future Architecture

Target:

```
Market

 |

Regime Detector

 |

Strategy Router

 |

Specialised Strategy

 |

Risk Engine

 |

Execution Layer

 |

Learning Feedback
```

---

Atlas is moving from a single strategy optimiser into a multi-strategy adaptive research platform.
# Atlas AI Trading Platform 3.5

# Project Status

Date:

August 2026

---

# Current Status

Atlas is operational.

The system can:

✅ Load historical market data

✅ Calculate indicators

✅ Generate signals

✅ Backtest strategies

✅ Optimise parameters

✅ Run multiprocessing optimisation

✅ Perform walk-forward validation

✅ Produce robustness reports

---

# Completed Milestones

## Atlas 1.x

Completed:

* Basic scanner
* Market data
* Indicators
* Signals

---

## Atlas 2.x

Completed:

* Portfolio system
* Risk management
* Trade models
* SQLite storage
* Dashboard
* Trade monitoring

---

## Atlas 3.x

Completed:

* Backtesting engine
* Strategy runner
* Optimisation framework
* Parallel optimisation
* Walk-forward validation
* Regime analysis

---

# Current Validation Results

Latest successful run:

```
Parameters:

score_threshold:
40

confidence:
0.4

ATR stop:
4.0

ATR target:
6.0
```

---

Performance:

```
Validation Windows:
5

Passed:
4

Failed:
1

Pass Rate:
80%

Robustness:
92/100
```

---

Combined validation:

```
Profit:
209286.64

Trades:
181

Win Rate:
67.4%

Profit Factor:
27.34
```

---

# Known Issue

One validation window still fails.

The failure occurs mainly during:

```
SIDEWAYS
NORMAL VOLATILITY
```

Current weakness:

* Range handling
* Strategy switching
* Market regime transitions

---

# Immediate Next Task

## 1. Complete Strategy Router

Implement:

```
Regime
 |
 v
StrategyRouter
 |
 + TrendStrategy
 |
 + RangeStrategy
 |
 + VolatilityStrategy
```

The router should:

* Select correct strategy
* Compare confidence
* Return strongest signal

---

## 2. Improve Regime Detection

Add:

* Confidence score
* Transition detection
* Volatility states

---

## 3. Re-run Walk Forward

Target:

```
90%+ pass rate
```

with:

* Lower drawdown
* Stable profit factor
* Consistent performance

---

# Development Rules

Always:

* Replace whole files when changing modules
* Keep architecture modular
* Test after changes
* Update this document after major milestones

---

# Current Development Priority

Priority order:

1. Strategy Router
2. Volatility Strategy
3. Regime confidence
4. Adaptive optimisation
5. Live monitoring

---

# Session Restart Instructions

Next session:

1. Read:

```
README.md
ARCHITECTURE.md
PROJECT_STATUS.md
```

2. Check:

```
strategy/
```

3. Continue from:

```
Strategy Router completion
```

Current Atlas state:

A working research platform ready for adaptive multi-strategy development.
