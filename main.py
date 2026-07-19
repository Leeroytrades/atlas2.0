"""
Atlas AI Trading Assistant 2.0
"""

from atlas.engine import AtlasEngine

from display.dashboard import show_dashboard


def main():

    atlas = AtlasEngine()

    print()

    print("Scanning Market...\n")

    results = atlas.scan_market()

    if not results:

        print("No symbols were scanned.")

        return

    best = results[0]

    score, trade = atlas.analyse(best.symbol)

    show_dashboard(
        results,
        score,
        trade,
    )


if __name__ == "__main__":
    main()