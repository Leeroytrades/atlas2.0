"""
Atlas AI Trading Platform 3.3

Validation Settings

Central configuration for
walk-forward research.
"""


# =====================================================
# Market
# =====================================================

SYMBOL = "SPY"

STARTING_CASH = 100000.0



# =====================================================
# Validation Mode
# =====================================================

# Available modes:
#
# quick
#   Development testing
#
# research
#   Medium validation run
#
# full
#   Complete research validation


MODE = "quick"



# =====================================================
# Window Configuration
# =====================================================

if MODE.lower() == "quick":


    TRAINING_SIZE = 500

    VALIDATION_SIZE = 100

    STEP_SIZE = 100

    MAX_WINDOWS = 3



elif MODE.lower() == "research":


    TRAINING_SIZE = 750

    VALIDATION_SIZE = 150

    STEP_SIZE = 150

    MAX_WINDOWS = 10



elif MODE.lower() == "full":


    TRAINING_SIZE = 1000

    VALIDATION_SIZE = 250

    STEP_SIZE = 250

    MAX_WINDOWS = None



else:


    raise ValueError(

        f"Unknown validation mode: {MODE}"

    )



# =====================================================
# Validation Rules
# =====================================================

MIN_VALIDATION_TRADES = 20

MIN_PROFIT_FACTOR = 1.2