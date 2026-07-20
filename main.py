"""
Atlas AI Trading Assistant 2.0
"""

from atlas.engine import AtlasEngine

from display.dashboard import show_dashboard



def main():

    atlas = AtlasEngine()


    print()

    print(
        "Scanning Market...\n"
    )


    results = atlas.scan_market()


    if not results:

        print(
            "No symbols were scanned."
        )

        return



    best = results[0]


    score, trade = atlas.analyse(
        best.symbol
    )


    if score is None:

        print()

        print(
            f"Existing position detected for {best.symbol}"
        )

        print(
            "Trade creation skipped."
        )

        print()

        print(
            atlas.performance()
        )

        return



    show_dashboard(

        results,

        score,

        trade,

        atlas.portfolio().positions,

        metrics=atlas.performance()

    )



if __name__ == "__main__":

    main()