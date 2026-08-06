# Atlas AI Trading Platform 4.0

# PROJECT_STATUS.md

## Complete Development Handover Document

Version: Atlas 4.0  
Status: Research Validation Phase  
Purpose: Full project continuation reference

---

# 1. PROJECT PURPOSE

Atlas AI Trading Platform is a modular quantitative research and trading development platform.

The original goal was to create an AI-assisted trading assistant capable of:

- scanning markets
- identifying opportunities
- analysing technical conditions
- generating trade ideas
- managing risk
- tracking positions

The project has evolved into a full research framework.

The current objective is not simply finding profitable historical strategies.

The objective is creating strategies that:

- survive unseen market data
- avoid overfitting
- maintain controlled drawdown
- demonstrate statistical robustness
- can eventually transition into paper trading and live execution


Core philosophy:

A strategy is not considered reliable because it made money historically.

A strategy is considered reliable only after surviving:

Historical testing

↓

Optimisation

↓

Walk Forward Validation

↓

Monte Carlo Simulation

↓

Research approval


---

# 2. CURRENT PROJECT STATE

Current version:

Atlas 4.0


Development phase:

Advanced research validation.


Overall completion estimate:

Approximately 85%.


Completed:

✓ Market data system

✓ Technical indicator pipeline

✓ Strategy framework

✓ Strategy routing

✓ Regime detection

✓ Risk management

✓ Position sizing

✓ Trade modelling

✓ Backtesting engine

✓ Trade simulator

✓ Performance metrics

✓ Parameter optimisation

✓ Parallel optimisation

✓ Walk forward validation

✓ Validation reporting

✓ Monte Carlo robustness testing


Remaining:

- Live data integration
- Paper trading engine
- Broker API integration
- Real-time execution monitoring
- Advanced AI explanation layer
- Production dashboard
- Portfolio optimisation across multiple assets


---

# 3. DEVELOPMENT HISTORY

## Atlas 1.0

Initial concept.

Purpose:

Create an AI trading assistant.

Features:

- Market scanning
- Technical indicators
- Basic signals


Limitations:

- No serious validation
- No optimisation framework
- No statistical testing


---

## Atlas 2.0

Major architecture improvement.

Introduced modular design.


Added:

- Trade objects
- Portfolio tracking
- SQLite database
- Risk management
- Dashboard
- Session management


Structure introduced:

data/

indicators/

strategy/

risk/

models/

database/

display/


---

## Atlas 3.0

Moved from trading assistant into quantitative research platform.


Added:

- Backtesting engine
- Historical simulation
- Performance analysis
- Strategy evaluation


---

## Atlas 3.3

Major validation upgrade.


Added:

- Optimisation framework
- Parallel processing
- Walk forward testing


First version capable of testing strategies on unseen data.


---

## Atlas 3.5

Research framework expansion.


Added:

- Validation windows
- Metrics extraction
- Validation database
- Regime awareness


---

## Atlas 4.0 CURRENT

Current research pipeline:

Market Data

↓

Indicators

↓

Regime Detection

↓

Strategy Selection

↓

Signal Generation

↓

Risk Management

↓

Trade Simulation

↓

Performance Analysis

↓

Optimisation

↓

Walk Forward Validation

↓

Monte Carlo Robustness


---

# 4. DEVELOPMENT ENVIRONMENT

Operating system:

Windows 11


Python:

Python 3.12.10


Environment:

.venv


Main tools:

VS Code

Git

GitHub


Installed packages:

pandas

numpy

yfinance

ta

rich

pytest

pyarrow


Repository:

Atlas


---

# 5. CURRENT DIRECTORY STRUCTURE

Main structure:

Atlas/

    atlas/

    data/

    indicators/

    strategy/

    risk/

    models/

    database/

    backtesting/

    optimisation/

    validation/

    research/

    display/

    main.py

    README.md

    ARCHITECTURE.md

    PROJECT_STATUS.md


---

# 6. SYSTEM ARCHITECTURE

Atlas follows a modular research architecture.


High-level flow:


Historical Data

↓

MarketData

↓

Indicator Engine

↓

Market Regime Detection

↓

Strategy Router

↓

Signal Generator

↓

Confidence Filtering

↓

Risk Manager

↓

Trade Object

↓

Simulator

↓

Metrics

↓

Optimiser

↓

Validation


Each stage is isolated to allow improvement without breaking the entire system.


---

# 7. DATA PIPELINE

Location:

data/


Main component:

MarketData


Purpose:

Retrieve and provide historical market information.


Current primary research asset:

SPY


Current dataset:

10 years

2512 daily candles


Data contains:

Open

High

Low

Close

Volume


Example:


SPY

2016-2026

2512 candles



---

# 8. INDICATOR SYSTEM

Location:

indicators/


Main function:

build_indicator_set()


Purpose:

Convert raw market data into analysis-ready data.


Current indicators:


## Trend

- SMA
- EMA 20
- EMA 50
- EMA 200
- ADX


## Momentum

- RSI
- MACD


## Volatility

- ATR
- Bollinger Bands


## Volume

- VWAP
- OBV
- CMF


Indicators are calculated before strategy processing.


---

# 9. STRATEGY SYSTEM

Location:

strategy/


Purpose:

Generate trading signals based on market conditions.


Architecture:


Market Condition

↓

Strategy Router

↓

Selected Strategy

↓

Signal


Signals contain:



signal

score

confidence



Example:



{
signal:"BUY",
score:70,
confidence:0.6
}



Score represents signal quality.

Confidence represents probability estimation.


---

# 10. REGIME DETECTION

Purpose:

Avoid trading unsuitable market environments.


Current categories:

TREND

RANGE

HIGH VOLATILITY

NORMAL VOLATILITY


Current filter behaviour:


Allowed:

- Trend markets
- Higher volatility opportunities


Blocked:

- Range markets


Reason:

Most false signals occur during sideways conditions.


---

# 11. BACKTESTING ENGINE

Location:

backtesting/


Main class:

BacktestEngine


Purpose:

Simulate strategy performance against historical data.


Current pipeline:


Data

↓

Indicators

↓

Regime Filter

↓

Strategy Router

↓

Signal Validation

↓

Risk Calculation

↓

Trade Creation

↓

Simulator

↓

Metrics


---

# 12. BACKTEST ENGINE FEATURES

Current features:


✓ Historical replay

✓ Indicator processing

✓ Strategy selection

✓ Score filtering

✓ Confidence filtering

✓ ATR based stops

✓ ATR based targets

✓ Position sizing

✓ Trade simulation

✓ Equity tracking

✓ Drawdown calculation


---

# 13. CURRENT BACKTEST RESULT

Example latest SPY research:


Dataset:

2512 candles


Trades:

106


Profit:

Approximately:

$39,912


Average trade:

Approximately:

$376


Win rate:

35.85%


Important:

Win rate is not the main metric.

The system focuses on:

- expectancy
- profit factor
- drawdown
- robustness


---

END OF THIS SECTION# 14. OPTIMISATION SYSTEM

Location:

optimisation/


Purpose:

Search thousands of possible strategy parameter combinations and identify robust parameter sets.


The optimiser does not simply search for maximum profit.

It ranks results using:


- Profit
- Profit factor
- Drawdown
- Trade quantity
- Win rate
- Stability
- Overfitting penalties


---

# 15. STRATEGY OPTIMIZER

Main class:

StrategyOptimizer


Responsibilities:


Generate configurations

↓

Run parallel tests

↓

Calculate ranking score

↓

Sort results

↓

Return best parameters


---

# 16. CURRENT OPTIMISATION PARAMETERS


Current search ranges:


## Score Threshold


40
50
60
70
80
90
100



## Confidence



0.4
0.5
0.6
0.7
0.8



## ATR Stop



2.0
2.5
3.0
3.5
4.0



## ATR Target



4.0
5.0
5.5
6.0



Total possible combinations:


700 tests


---

# 17. PARALLEL OPTIMISATION

Location:

optimisation/parallel_runner.py


Purpose:

Speed up optimisation using multiprocessing.


Current configuration:



Workers: 16
Tests: 700



Instead of:

one configuration

↓

wait

↓

next configuration


Atlas runs:


configuration 1

configuration 2

configuration 3

...

configuration 700


simultaneously.


---

# 18. OPTIMISATION RESULT

Latest successful optimisation:


Locked Parameters:



Score Threshold:
60

Confidence:
0.4

ATR Stop:
2.5

ATR Target:
6.0



These parameters were NOT accepted immediately.

They were passed into validation.


---

# 19. WALK FORWARD VALIDATION

Location:

validation/


Purpose:

Prevent overfitting.


Traditional backtesting:


Train

↓

Test


Problem:

The strategy may simply memorise history.


Walk forward:


Historical Data


↓

Training Window


↓

Optimisation


↓

LOCK PARAMETERS


↓

Future unseen window


↓

Measure performance


---

# 20. WALK FORWARD ENGINE

Main class:

WalkForwardValidator


Current settings:



Symbol:
SPY

Training size:
1000 candles

Validation size:
250 candles

Step:
250 candles

Windows:
6 generated

Testing:
3 windows



---

# 21. VALIDATION RESULTS

Latest run:



Windows Tested:
3

PASS:
2

FAIL:
1



Result:



PASS RATE:
66.6%



This is a significant milestone.


A strategy that passes unseen data has much higher credibility than one that only performs well during optimisation.


---

# 22. VALIDATION VERDICT LOGIC


Current PASS requirement:


Validation must have:



Net Profit > 0

AND

Profit Factor >= 1.2



If conditions fail:



FAIL



Future improvement:

Add additional requirements:


- minimum trades
- drawdown limit
- consistency score
- Monte Carlo requirement


---

# 23. VALIDATION DATABASE

Location:


database/


Purpose:


Store historical validation results.


Stores:


- Parameters
- Training metrics
- Validation metrics
- Regime information
- Verdict


Allows comparison between strategy versions.


---

# 24. REGIME AWARE VALIDATION


Validation includes market context.


Example:



Market Regime:

TREND

Volatility:

NORMAL

Momentum:

NEUTRAL



Purpose:

Understand when strategies work and when they fail.


---

# 25. MONTE CARLO ROBUSTNESS TESTING

Location:

research/monte_carlo.py


Purpose:

Determine whether results depend on lucky trade ordering.


A profitable strategy may appear strong only because its biggest wins happened early.


Monte Carlo removes this possibility.


Process:


Historical Trades

↓

Random resampling

↓

Thousands of possible trade sequences

↓

Equity reconstruction

↓

Risk analysis


---

# 26. CURRENT MONTE CARLO IMPLEMENTATION


Test:



Trades:
106

Simulations:
10,000



Method:


Bootstrap sampling.


Each simulation:

- randomly selects trades
- creates a new sequence
- calculates return
- calculates drawdown


---

# 27. LATEST MONTE CARLO RESULTS


Latest run:



Simulations:
10000

Trades Tested:
106



Return Distribution:



Average Profit:
$40,040.41

Median Profit:
$39,871.57

Worst Case:
-$14,199.87

Best Case:
$100,703.89

5th Percentile:
$18,686.36

95th Percentile:
$61,545.92



---

# 28. MONTE CARLO RISK RESULTS



Average Drawdown:
4.82%

Worst Drawdown:
23.12%

Loss Probability:
0.08%

DD Failure Probability:
0.00%



---

# 29. TRADE QUALITY RESULTS



Average Trade:
$376.53

Win Rate:
35.85%



Important:


Low win rate does not automatically mean poor strategy.


The system relies on:


average winner size

average loser size

expectancy

risk control


---

# 30. ROBUSTNESS SCORE


Latest:



84.92 / 100



Interpretation:


90-100:

Excellent


75-90:

Strong


60-75:

Needs improvement


Below 60:

Weak


Current result:


STRONG


---

# 31. IMPORTANT DISCOVERY


Earlier Monte Carlo versions were misleading.


They produced:



Worst Profit:
same as best profit

Loss Probability:
0%



Reason:


The implementation only shuffled existing trades.


This preserved total profit exactly.


The system was fixed by introducing:


bootstrap sampling:



random.choices()



Now simulations produce realistic distributions.


---

# 32. CURRENT PROJECT QUALITY ASSESSMENT


Atlas has moved beyond a simple trading bot.


It is now a quantitative research framework.


Current maturity:


Architecture:

★★★★★


Backtesting:

★★★★☆


Optimisation:

★★★★☆


Validation:

★★★★☆


Statistical testing:

★★★★☆


Execution:

★☆☆☆☆


---

# 33. WHITE PAPER READINESS


Current status:


Approximately:

70-80% ready for research paper structure.


Available evidence:


✓ Strategy architecture

✓ Validation methodology

✓ Optimisation process

✓ Walk-forward results

✓ Monte Carlo testing

✓ Risk analysis


Missing:


- More assets
- Longer testing period
- Multiple market regimes
- Benchmark comparison
- Transaction cost analysis
- Paper trading evidence


---

# 34. CURRENT KNOWN ISSUES


## Issue 1

BacktestEngine loads market data repeatedly during optimisation.


Effect:


Large console output:



Loading historical data: SPY
Loaded candles: 2512



Solution:

Cache datasets before optimisation workers start.


Priority:

HIGH


---

## Issue 2

Runtime warning:



validation.walk_forward found in sys.modules



Cause:


Python module import behaviour.


Impact:


Minimal.


Not currently affecting results.


---

## Issue 3

Multiprocessing complexity.


Workers must receive serialisable objects.


Previous issue:



tuple object has no attribute get



Cause:


Configuration format mismatch.


Fixed by standardising optimiser configurations.


---

## Issue 4

Strategy still tested mainly on SPY.


Need expansion:


- QQQ
- DIA
- IWM
- individual stocks
- futures


---

# 35. IMMEDIATE NEXT TASKS


Priority order:


## 1. Data caching


Remove repeated:



Loading historical data



during optimisation.


Expected improvement:

Much faster optimisation.


---

## 2. Add benchmark comparison


Compare Atlas against:


Buy and Hold SPY


Random strategy


Simple moving average


---

## 3. Add transaction costs


Include:


commission

slippage

spread


---

## 4. Expand validation


Run:


10+ windows

multiple symbols


---

## 5. Paper trading engine


Before live execution:


Market data

↓

Signal

↓

Virtual order

↓

Portfolio tracking


---

END OF SECTION# 36. COMPLETE PROJECT ARCHITECTURE


Atlas is divided into independent modules.


The design principle:


Every component should be replaceable without rebuilding the entire system.


---

# ROOT DIRECTORY



Atlas/

main.py

README.md

ARCHITECTURE.md

PROJECT_STATUS.md

requirements.txt



Purpose:


Application entry points and documentation.


---

# 37. atlas/


Purpose:


Core application framework.


Contains:


- Engine control
- Application state
- Session handling


Responsible for connecting:


Market

↓

Analysis

↓

Decision


---

# 38. data/


Purpose:


Market information layer.


Main component:



MarketData



Responsibilities:


- Download historical data
- Return DataFrames
- Handle symbols
- Manage datasets


Current provider:


Yahoo Finance through yfinance.


Future:


Replaceable with:

- Polygon
- Interactive Brokers
- Alpaca
- Binance
- CME feeds


---

# 39. indicators/


Purpose:


Technical analysis engine.


Main component:



build_indicator_set()



Input:


Raw OHLCV


Output:


Enhanced DataFrame containing:


- Trend
- Momentum
- Volatility
- Volume indicators


---

# 40. strategy/


Purpose:


Trading decision engine.


Contains:


## router.py


Selects strategy based on market regime.


## regime_filter.py


Controls allowed environments.


## Individual strategies


Generate signals.


Signal format:



{
signal,
score,
confidence
}



---

# 41. risk/


Purpose:


Capital protection.


Responsibilities:


- Position sizing
- Risk calculation
- Stop placement
- Reward calculation


Current approach:


ATR based risk management.


---

# 42. models/


Purpose:


Data objects.


Important models:


## Trade


Represents a complete trade.


Contains:



symbol

direction

entry

stop_loss

take_profit

quantity

confidence

status

profit_loss



---

# 43. backtesting/


Purpose:


Historical simulation.


Main components:


## engine.py


Controls research pipeline.


## simulator.py


Simulates individual trades.


Outputs:


- Trades
- Equity curve
- Drawdown
- Performance


---

# 44. optimisation/


Purpose:


Parameter discovery.


Contains:


## optimizer.py


Generates and ranks configurations.


## parallel_runner.py


Runs configurations concurrently.


Current performance:


700 tests

16 workers


---

# 45. validation/


Purpose:


Scientific testing.


Contains:


## walk_forward.py


Main validation engine.


## window.py


Creates training/testing periods.


## metrics.py


Calculates validation statistics.


## report.py


Displays results.


---

# 46. research/


Purpose:


Advanced statistical analysis.


Current modules:


## monte_carlo.py


Robustness testing.


Future additions:


- correlation analysis
- regime research
- feature importance
- machine learning experiments


---

# 47. database/


Purpose:


Persistent storage.


Current:


SQLite


Stores:


- Trades
- Validation results


Future:


Research database containing:


- Every optimisation run
- Every experiment
- Strategy versions


---

# 48. display/


Purpose:


User interface.


Current:


Terminal dashboards.


Future:


Web interface.


Possible technologies:


- Streamlit
- React
- FastAPI


---

# 49. CURRENT COMMANDS


Activate environment:


Windows:



.venv\Scripts\activate



---

Run main application:



python main.py



---

Run walk-forward validation:



python -m validation.walk_forward



---

Start Python research console:



python



---

Run Monte Carlo:


```python
from backtesting.engine import BacktestEngine
from research.monte_carlo import MonteCarloAnalyzer, print_monte_carlo_report


engine = BacktestEngine()

result = engine.run("SPY")


mc = MonteCarloAnalyzer()

report = mc.run(
    result["trade_list"],
    simulations=10000
)


print_monte_carlo_report(report)
50. CURRENT BEST KNOWN CONFIGURATION

Validated parameters:

Score Threshold:
60


Confidence:
0.4


ATR Stop:
2.5


ATR Target:
6.0

These parameters currently represent the strongest discovered configuration.

They are NOT yet live trading parameters.

They require:

more validation
paper trading
broader testing
51. DEVELOPMENT RULES GOING FORWARD

When modifying Atlas:

Rule 1

Do not remove validation.

Profit alone is meaningless.

Every improvement must pass:

backtest
walk forward
robustness testing
Rule 2

Avoid overfitting.

Do not tune parameters endlessly against SPY.

Rule 3

Prefer modular improvements.

Add new modules instead of rewriting working components.

Rule 4

Keep research reproducible.

Every experiment should record:

parameters
dataset
results
date
version
52. CURRENT BOT VS FUTURE PLATFORM

Current:

Research engine.

Not yet:

Autonomous trading system.

The difference:

A bot:

"Buy because indicator says buy."

Atlas:

"Analyse market, evaluate conditions, test strategy statistically, estimate confidence, control risk."

53. ROADMAP TO LIVE SYSTEM
Phase 1 COMPLETE

Research foundation.

✓

Phase 2 CURRENT

Validation.

Tasks:

More assets
More windows
Benchmark tests
Phase 3

Paper trading.

Build:

Live market feed
Virtual account
Order simulation
Daily reporting
Phase 4

Execution.

Integrate:

Broker API
Position management
Real-time risk
Phase 5

AI layer.

Add:

Natural language explanations
Research assistant
Strategy review
Market summaries
54. TOMORROW START CHECKLIST

When continuing:

Open Atlas folder.

Activate environment:

.venv\Scripts\activate

Check status:

git status

Run:

python -m validation.walk_forward

Confirm:

PASS: 2/3

Run Monte Carlo.

Expected:

Trades:
106


Robustness:
~85/100
55. FIRST IMPROVEMENT TOMORROW

Recommended order:

Step 1

Implement dataset caching.

Reason:

Current optimisation repeatedly downloads SPY.

This wastes time.

Step 2

Create ResearchRunner.

Purpose:

One command:

python research/run_experiment.py

Runs:

Backtest

Optimisation

Validation

Monte Carlo

Report generation

Step 3

Generate formal research report.

Output:

PDF / Markdown:

Methodology
Results
Statistics
Limitations
56. CURRENT ACHIEVEMENT SUMMARY

Atlas has successfully progressed from:

Simple trading assistant

to:

Quantitative research platform.

Major achievements:

✓ Modular architecture

✓ Real historical testing

✓ Strategy optimisation

✓ Parallel computing

✓ Walk-forward validation

✓ Monte Carlo robustness testing

The project has reached the point where the next improvements are scientific refinement rather than basic construction.

57. FINAL STATUS

Current classification:

ADVANCED RESEARCH PROTOTYPE

Confidence level:

Promising but not production ready.

Evidence:

Strong.

Requirements before live capital:

Multi-market validation

Paper trading

Transaction cost modelling

Long-term monitoring

Risk review

END OF PROJECT STATUS

Atlas AI Trading Platform 4.0

Last known state:

Validation successful.

Monte Carlo robustness completed.

Ready for next research phase.


That is the completed handover document. Save it as:


PROJECT_STATUS.md


Tomorrow we can continue from this point without needing to resend the project files.