# Atlas AI Trading Assistant 3.0

# System Architecture

## Overview

Atlas is a modular algorithmic trading research and execution platform.

The design separates:

* Data acquisition
* Market analysis
* Strategy generation
* Risk management
* Trade execution
* Portfolio management
* Persistence
* Reporting
* Backtesting
* Optimisation

The goal is to evolve Atlas from a trading assistant into a complete quantitative research and execution framework.

---

# High Level Architecture

```text
                    USER
                     |
                     |
                 main.py
                     |
                     |
              AtlasEngine
                     |
     --------------------------------
     |              |               |
 Session        Services        Database
     |              |               |
     |              |               |
 Portfolio     Trading Logic     SQLite
 Watchlist     Monitoring
               Execution
               Analytics


Market Data
     |
     |
Indicators
     |
     |
Strategy Engine
     |
     |
Signal Generation
     |
     |
Risk Manager
     |
     |
Trade Creation
     |
     |
Execution / Paper Trading
     |
     |
Portfolio + Database
```

---

# Core Application Layer

## main.py

Application entry point.

Responsibilities:

* Start Atlas
* Initialise engine
* Run scheduler
* Display output

Flow:

```text
main.py
    |
    v
AtlasEngine
```

---

# Atlas Core

## atlas/

The central application package.

---

## atlas/engine.py

The main orchestration layer.

Responsibilities:

* Initialise services
* Connect modules
* Manage application lifecycle

Current dependencies:

```text
AtlasEngine
 |
 |-- Scanner Service
 |-- Trade Service
 |-- Portfolio Service
 |-- Monitoring Service
 |-- Performance Service
 |-- Paper Trading Service
 |-- Backtesting Service
```

The engine should coordinate modules.

Business logic should remain outside the engine.

---

## atlas/session.py

Runtime session management.

Stores:

* active watchlist
* current state
* runtime information

---

## atlas/watchlist.py

Dynamic market list management.

Supports:

* loading symbols
* adding symbols
* removing symbols
* saving changes

---

## atlas/portfolio.py

Portfolio state model.

Tracks:

* balance
* positions
* exposure
* active trades

---

# Data Layer

## data/

Responsible for external market information.

---

## data/market_data.py

Provides:

* historical prices
* candle data
* market information

Current provider:

yfinance

Future:

* broker feeds
* websocket data
* live exchange feeds

---

# Indicator System

## indicators/

Technical analysis engine.

---

## indicators/composite.py

Creates combined indicator sets.

Current indicators:

* EMA
* ATR
* Momentum
* Volume analysis

Output feeds:

```text
Indicators
    |
    v
Strategy Engine
```

---

# Strategy Layer

## strategy/

Responsible for trading decisions.

---

## strategy/signal_generator.py

Creates Atlas scorecards.

Outputs:

* score
* bias
* confidence
* signal

Example:

```text
Score:
90

Bias:
BUY

Confidence:
0.9
```

---

# Risk Management

## risk/

Controls trade safety.

---

## risk/risk_manager.py

Responsible for:

* position sizing
* stop calculation
* reward calculation
* risk percentage

Current model:

ATR based risk.

---

## risk/trade.py

Trade object.

Stores:

* symbol
* direction
* entry
* stop
* target
* quantity
* risk
* reward
* confidence
* lifecycle state

---

# Service Layer

## services/

Contains application business services.

---

## scanner_service.py

Runs:

```text
Market Data
      |
Indicators
      |
Strategy
      |
Signals
```

---

## trade_service.py

Responsible for:

* opening trades
* closing trades
* trade lifecycle

---

## paper_trading_service.py

Simulates execution.

Used before real broker connection.

---

## execution_service.py

Handles:

* broker positions
* monitoring
* execution state

---

## monitoring_service.py

Monitors:

* active positions
* stop loss
* take profit
* alerts

---

## performance_service.py

Calculates:

* returns
* win rate
* drawdown
* profitability

---

# Database Layer

## database/

Persistence system.

Uses:

SQLite

---

## database/database.py

Database connection.

---

## database/trades.py

Trade persistence.

Stores:

* entries
* exits
* profit/loss
* status

Database file:

```text
atlas.db
```

---

# Alert System

## alerts/

Notification framework.

Current:

Console alerts

Future:

* Email
* Telegram
* Mobile notifications
* Discord

---

# Backtesting System

## backtesting/

Historical strategy testing framework.

---

## historical_data.py

Loads historical candles.

---

## strategy_runner.py

Runs Atlas strategy over historical data.

Flow:

```text
Historical Candle
        |
Indicators
        |
Scorecard
        |
Signal
```

Supports:

* score threshold
* confidence threshold

---

## simulator.py

Trade simulator.

Features:

* ATR stops
* ATR targets
* trailing stops
* slippage
* commission
* equity tracking

---

## engine.py

Backtest controller.

Handles:

* signals
* trade creation
* lifecycle

---

## analytics.py

Ranks performance.

Measures:

* profit
* win rate
* reliability

---

## multi_engine.py

Future multi-symbol testing.

---

# Optimisation System

## optimisation/

Strategy discovery framework.

---

## optimizer.py

Searches parameter combinations.

Current parameters:

```text
Score threshold

Confidence

ATR Stop

ATR Target
```

Current search:

768 combinations.

Output:

Best performing configurations.

Future:

* genetic optimisation
* machine learning optimisation
* reinforcement learning

---

# Data Flow

## Live Trading Flow

```text
Market Data
     |
     v
Indicators
     |
     v
Strategy Score
     |
     v
Signal
     |
     v
Risk Manager
     |
     v
Trade
     |
     v
Execution
     |
     v
Portfolio
     |
     v
Database
```

---

## Backtesting Flow

```text
Historical Data
        |
        v
Strategy Runner
        |
        v
Signals
        |
        v
Simulator
        |
        v
Analytics
        |
        v
Optimiser
```

---

# Design Principles

Atlas follows:

## Separation of Responsibility

Each module should have one purpose.

Example:

Bad:

```text
engine.py calculates indicators
```

Good:

```text
indicator module calculates indicators
engine coordinates modules
```

---

## Replaceability

Components should be replaceable.

Example:

Current:

```text
Yahoo Finance
```

Future:

```text
Broker API
Exchange Feed
```

without rewriting the strategy engine.

---

## Testing First

Every major feature should have:

* isolated test
* backtest validation
* live paper validation

---

# Current Architecture Status

## Complete

✅ Modular structure
✅ Service layer
✅ Database layer
✅ Risk system
✅ Paper trading
✅ Backtesting
✅ Optimisation framework

---

# Future Architecture Goals

## Phase 1

Strategy improvement:

* better entries
* short trades
* market regimes

## Phase 2

Intelligence:

* AI explanations
* adaptive parameters
* self optimisation

## Phase 3

Execution:

* broker integration
* live feeds
* automated trading

## Phase 4

Platform:

* web dashboard
* cloud deployment
* multi-user support

---

# Development Rule

Atlas should grow by adding modules, not by making existing files larger.

Keep:

* engine as coordinator
* services as logic
* models as data
* database as storage
* strategies as independent components

This keeps Atlas scalable.
