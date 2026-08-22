Atlas AI Trading Platform
Professional Algorithmic Trading Research Platform

Version: 4.0 Development Branch

Overview

Atlas AI Trading Platform is a modular quantitative trading research system designed to investigate, validate and improve algorithmic trading strategies.

The project has evolved from a simple market scanner into a complete research pipeline containing:

Market data acquisition
Technical analysis
Signal generation
Strategy routing
Market regime detection
Risk management
Backtesting
Strategy optimisation
Walk-forward validation
Monte Carlo robustness testing
Research reporting

The core philosophy is:

A strategy is not considered valid because it made money historically. It must survive optimisation, unseen data testing and robustness analysis.

Atlas is designed around professional quantitative research principles:

Avoid overfitting.
Test on unseen data.
Validate parameter stability.
Measure downside risk.
Separate research from live execution.
Current Development Status
Completed Systems
Market Data

Implemented:

Historical data loading
Multi-symbol support
Data preparation pipeline
Indicator integration

Current primary research market:

Symbol:
SPY

Dataset:
10 years daily data

Candles:
2512
Technical Analysis Engine

Implemented indicators:

Trend
SMA
EMA
ADX
Trend strength
Momentum
RSI
MACD
Volatility
ATR
Bollinger Bands
Volume
OBV
CMF
VWAP

Indicators are combined through:

indicators/composite.py
Strategy System

Atlas uses a modular strategy architecture.

Pipeline:

Market Data

↓

Indicators

↓

Regime Detection

↓

Strategy Router

↓

Strategy Selection

↓

Signal Generation

↓

Validation

↓

Trade Creation

Strategies are selected dynamically depending on market conditions.

Regime Detection

Implemented:

Trend detection
Range detection
Volatility filtering

Purpose:

Avoid forcing the wrong strategy into unsuitable market conditions.

Example:

Trending market:

Trend Strategy

Sideways market:

Range Strategy

High volatility:

Risk adjusted behaviour
Backtesting Engine

Location:

backtesting/

Pipeline:

Historical Candles

↓

Indicators

↓

Regime Filter

↓

Strategy Router

↓

Signal

↓

Risk Calculation

↓

Trade Object

↓

Simulator

↓

Performance Metrics

Current features:

Long trades
Short trades
ATR stops
ATR targets
Position sizing
Equity tracking
Drawdown calculation
Trade history
Strategy Optimisation

Location:

optimisation/

The optimiser searches parameter combinations.

Current parameters:

Signal Score
40-100
Confidence
0.4-0.8
ATR Stop
2.0-4.0
ATR Target
4.0-6.0

Current optimisation:

700 configurations
16 parallel workers

Ranking considers:

Profit
Profit factor
Drawdown
Trade quantity
Win rate
Overfit protection
Walk Forward Validation

Location:

validation/

Purpose:

Test whether optimised parameters survive unseen market conditions.

Workflow:

Historical Data

↓

Training Window

↓

Optimisation

↓

Lock Parameters

↓

Validation Window

↓

Performance Test

↓

PASS / FAIL

Current configuration:

Training:
1000 candles

Validation:
250 candles

Step:
250 candles

Windows:
6 generated

Testing:
3 windows

Recent result:

PASS: 2/3
FAIL: 1/3

This is a significant milestone because the strategy is no longer simply curve-fitted.

Monte Carlo Analysis

Location:

research/monte_carlo.py

Purpose:

Determine whether performance depends on lucky trade ordering.

Method:

Take historical trades.
Bootstrap sample trade results.
Randomise order.
Rebuild equity curves.
Measure outcomes.

Metrics:

Average return
Median return
Worst case
Best case
5th percentile
95th percentile
Drawdown probability
Loss probability
Robustness score

Latest meaningful result:

Trades Tested:
106

Average Profit:
$40,040

Median Profit:
$39,871

Worst Case:
-$14,199

Best Case:
$100,703

5th Percentile:
$18,686

95th Percentile:
$61,545

Average Drawdown:
4.82%

Worst Drawdown:
23.12%

Loss Probability:
0.08%

Robustness Score:
84.92/100

Interpretation:

The strategy appears robust but requires more validation before any live deployment.

Current Project Goal

Move from:

Working backtester

to:

Professional quantitative research platform

Remaining major stages:

Improve validation depth.
Add multi-market testing.
Add strategy comparison framework.
Add research reports.
Add paper trading layer.
Add live execution architecture.
Produce white paper documentation.
Development Principles

Atlas should always prioritise:

Reliability over speed.
Validation over optimisation.
Robustness over maximum profit.
Simplicity over unnecessary complexity.

A lower return strategy that survives testing is preferable to a high return strategy that collapses out-of-sample.

Repository Structure
Atlas/

atlas/
    core engine

backtesting/
    engine
    simulator

data/
    market loading

indicators/
    technical indicators

strategy/
    strategies
    router
    filters

risk/
    position sizing

optimisation/
    optimiser
    parallel runner

validation/
    walk forward system
    metrics
    reports

research/
    monte carlo
    analysis tools

database/
    persistence

display/
    dashboard

models/
    trade objects
Next Development Session

Recommended order:

Review validation results.
Add automated research reports.
Improve Monte Carlo integration.
Add multi-symbol validation.
Begin white paper preparation.