Atlas AI Trading Platform Architecture

Version 4.0

System Philosophy

Atlas is designed as a research-first quantitative trading platform.

The architecture separates:

Data
Analysis
Strategy
Risk
Simulation
Validation
Research

Each layer has a defined responsibility.

High Level Architecture
                 USER

                  |

               main.py

                  |

             Atlas Engine

                  |

        ----------------------

        |                    |

   Research Pipeline     Live Pipeline



Research Pipeline
Market Data

↓

Data Processing

↓

Indicator Engine

↓

Regime Detection

↓

Strategy Router

↓

Signal Generation

↓

Risk Engine

↓

Trade Model

↓

Simulator

↓

Performance Metrics

↓

Optimisation

↓

Validation

↓

Research Reports
Core Modules
Data Layer

Location:

data/

Responsible for:

Market downloads
Historical candles
Data formatting

Main class:

MarketData
Indicator Layer

Location:

indicators/

Responsible for:

Technical calculations
Feature generation

Output:

Enhanced dataframe containing:

Price
Volume
Trend metrics
Momentum metrics
Volatility metrics
Strategy Layer

Location:

strategy/

Contains:

router.py

Chooses appropriate strategy.

Strategies receive:

Market data
Indicators
Regime information

Return:

signal
score
confidence
Risk Layer

Responsible for:

Position sizing
Stop placement
Target placement
Capital protection

Current model:

ATR based risk.

Backtesting Layer

Location:

backtesting/

Components:

engine.py

simulator.py

Engine:

Controls research execution.

Simulator:

Controls trade outcome simulation.

Optimisation Layer

Location:

optimisation/

Components:

optimizer.py

parallel_runner.py

Purpose:

Search parameter space.

Uses:

ProcessPoolExecutor

Current:

16 workers
Validation Layer

Location:

validation/

Components:

walk_forward.py

window.py

metrics.py

report.py

Purpose:

Prevent overfitting.

Research Layer

Location:

research/

Contains:

monte_carlo.py

Purpose:

Statistical robustness testing.

Current Data Flow

Example:

SPY candles

↓

MarketData

↓

build_indicator_set()

↓

RegimeFilter

↓

StrategyRouter

↓

Signal

↓

Trade()

↓

Simulator

↓

Metrics

↓

Optimizer

↓

Walk Forward

↓

Monte Carlo

↓

Report
Future Architecture

Planned:

Live Market Data

↓

Real Time Engine

↓

Signal Service

↓

Risk Service

↓

Broker API

↓

Execution Engine

↓

Portfolio Manager

↓

Monitoring Dashboard
White Paper Architecture

Eventually document:

Strategy philosophy
Research methodology
Validation methodology
Optimisation process
Risk framework
Monte Carlo analysis
Limitations
Future improvements
Important Design Rules

Never:

Optimise and test on same data.
Trust single backtests.
Deploy without validation.
Judge strategy on profit alone.

Always:

Test unseen periods.
Measure drawdown.
Analyse robustness.
Track failures.