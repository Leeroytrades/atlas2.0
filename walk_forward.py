"""
Atlas Walk Forward Runner
"""

from research.dataset_cache import DatasetCache

from research.walk_forward import WalkForwardValidator



def main():


    symbol = "SPY"


    cache = DatasetCache()


    data = cache.load(

        symbol

    )


    validator = WalkForwardValidator()


    validator.run(

        symbol,

        data

    )



if __name__ == "__main__":

    main()