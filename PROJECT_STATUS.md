# Atlas AI Trading Platform 3.3

## Project Status & Architecture Handover

**Project:** Atlas AI Trading Platform
**Current Version:** 3.3
**Repository Branch:** `refactor/atlas-2.1`
**Latest Commit:** `93884c0 - Atlas 3.3 complete - optimisation and walk forward validation`
**Environment:** Windows 11 / Python 3.12 / Virtual Environment `.venv`

---

# 1. Project Vision

Atlas is a modular AI-assisted trading research and execution platform.

The long-term goal is to create a complete trading intelligence system capable of:

* Market scanning
* Technical analysis
* Signal generation
* Risk management
* Portfolio tracking
* Trade execution simulation
* Backtesting
* Strategy optimisation
* Walk-forward validation
* Market regime detection
* AI-generated explanations
* Live market monitoring

Current focus is research quality:

* Avoid overfitting
* Discover robust parameters
* Validate strategies on unseen data
* Build institutional-style research workflow

---

# 2. Current Development Stage

## COMPLETED

### Atlas Core Engine

✅ Market data loading
✅ Indicator generation
✅ Composite scoring system
✅ Signal generation
✅ Trade creation
✅ Risk management
✅ Position sizing
✅ Portfolio tracking
✅ SQLite persistence
✅ Dashboard output

---

## Completed Research Engine

### Optimisation System

Location:

```
optimisation/
```

Files:

```
optimizer.py
parallel_runner.py
worker.py
results.py
results_database.py
results.db
```

Capabilities:

* Generates parameter combinations
* Runs parallel optimisation
* Scores configurations
* Saves results
* Ranks strategies

Current tested optimisation:

400 configurations

Parameters:

```
Score threshold
Confidence threshold
ATR stop multiplier
ATR target multiplier
```

Best discovered configuration:

```
Score:
40

Confidence:
0.4-0.5

ATR Stop:
4.25

ATR Target:
5.0
```

Example optimisation result:

```
Starting Cash:
100000

Ending Equity:
319840.94

Profit:
219840.94

Trades:
412

Win Rate:
34.95%

Profit Factor:
2.59
```

Important:
This is an optimisation result only.
It is NOT considered validated until walk-forward testing passes.

---

# 3. Walk Forward Validation Engine

Location:

```
validation/
```

Files:

```
walk_forward.py
window.py
metrics.py
report.py
robustness.py
settings.py
```

Purpose:

Prevent overfitting.

Workflow:

```
Historical Data

        ↓

Training Window

        ↓

Optimisation

        ↓

Lock Parameters

        ↓

Unseen Validation Window

        ↓

Performance Evaluation

        ↓

PASS / FAIL
```

---

## Current Walk Forward Configuration

Example:

Training:

```
500 candles
```

Validation:

```
100 candles
```

Step:

```
100 candles
```

Expanding:

```
True
```

---

# 4. Current Validation Results

Current status:

```
PASS: 0 / 10
```

Validation is currently FAILING.

This is expected and is the next important development area.

Observed issue:

Optimisation performs extremely well:

Example:

```
Training profit:
90641

Profit Factor:
12.24
```

But unseen validation:

```
0 trades
or
negative results
```

Meaning:

The strategy is likely overfitting training data.

---

# 5. Current Known Problems

## Problem 1

Optimiser finds unrealistic high-performing configurations.

Example:

```
Profit:
$219k

PF:
2.59
```

but walk-forward fails.

Likely causes:

* Too many parameters
* Weak validation rules
* Insufficient market regimes
* Strategy adapts too much to historical data

---

## Problem 2

Some validation windows produce:

```
total_trades = 0
```

Need investigation.

Possible causes:

* Regime filter too restrictive
* Confidence threshold too high
* Score requirements too strict
* Signal generator behaves differently on unseen data

---

## Problem 3

Training metrics appear suspicious.

Example:

```
winning_trades = 0
losing_trades = 0
win_rate = 64%
```

Needs checking.

Possible issue:

ValidationMetrics mapping may not correctly read BacktestEngine results.

---

# 6. Current Architecture

```
Atlas/

│
├── main.py
│
├── atlas/
│   ├── engine.py
│   ├── session.py
│   ├── portfolio.py
│   └── watchlist.py
│
├── data/
│   └── market_data.py
│
├── indicators/
│   ├── composite.py
│   ├── trend.py
│   ├── momentum.py
│   ├── volatility.py
│   └── volume.py
│
├── strategy/
│   └── signal_generator.py
│
├── models/
│   └── scorecard.py
│
├── risk/
│   ├── risk_manager.py
│   └── trade.py
│
├── backtesting/
│   └── engine.py
│
├── optimisation/
│   ├── optimizer.py
│   ├── parallel_runner.py
│   ├── worker.py
│   ├── results.py
│   └── results_database.py
│
├── validation/
│   ├── walk_forward.py
│   ├── window.py
│   ├── metrics.py
│   ├── report.py
│   └── robustness.py
│
├── research/
│   ├── regime_detector.py
│   ├── dataset_builder.py
│   ├── dataset_cache.py
│   ├── score_builder.py
│   └── walk_forward.py
│
└── database/
    ├── database.py
    ├── trades.py
    ├── portfolio.py
    ├── equity.py
    └── validation.py

```

---

# 7. Database

Current database:

```
atlas.db
```

Location:

```
C:\Users\Admin\Atlas\atlas.db
```

Used for:

* Trades
* Equity history
* Validation results
* Portfolio data

Optimisation database:

```
optimisation/results.db
```

Stores:

* Tested configurations
* Performance metrics
* Rankings

---

# 8. Current Technology Stack

Python:

```
3.12
```

Libraries:

```
pandas
numpy
yfinance
ta
rich
pytest
pyarrow
```

Environment:

```
.venv
```

---

# 9. Current Git Status

Branch:

```
refactor/atlas-2.1
```

Latest commits:

```
93884c0
Atlas 3.3 complete - optimisation and walk forward validation

53f74a7
Atlas 3.1 research engine milestone
```

Working tree:

```
clean
```

---

# 10. Cleanup Completed

Removed:

* Python cache files
* `.pyc` files

Checked:

```
*.log
*.bak
```

No unnecessary files found.

---

# 11. Immediate Next Development Tasks

Priority order:

## 1. Fix Walk Forward Validation

Investigate:

* Why optimisation does not transfer
* Why validation creates no trades
* Whether regime filter is too aggressive

---

## 2. Fix Validation Metrics

Confirm:

* Trade counting
* Win/loss calculation
* Drawdown calculation
* Profit factor calculation

---

## 3. Improve Optimisation

Possible improvements:

* Add minimum validation trades requirement
* Penalise unstable strategies
* Optimise across multiple symbols
* Add different market regimes
* Add out-of-sample scoring

---

## 4. Add Robustness Testing

Examples:

* Different symbols
* Different time periods
* Monte Carlo simulation
* Parameter sensitivity testing

---

# 12. Current Atlas Development Philosophy

Do NOT optimise for maximum historical profit.

Goal:

Find strategies that survive unseen market conditions.

A good Atlas strategy should have:

* Consistent returns
* Reasonable drawdown
* Stable parameters
* Multiple market regimes
* Repeatable performance

---

# 13. Tomorrow's Starting Point

Start by checking:

1. `validation/walk_forward.py`
2. `validation/metrics.py`
3. `backtesting/engine.py`
4. `strategy/signal_generator.py`

Main question:

"Why does the optimiser find profitable strategies that fail immediately on unseen data?"

The next milestone is not higher backtest profit.

The next milestone is:

A strategy that passes walk-forward validation consistently.

---

END OF STATUS
