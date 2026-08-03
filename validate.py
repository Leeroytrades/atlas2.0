"""
Atlas AI Trading Platform 3.3

Validation Entry Point

Runs:

1. Walk forward validation
2. Validation report
3. Robustness analysis
"""

from __future__ import annotations


from validation.walk_forward import WalkForwardValidator

from validation.report import ValidationReport

from validation.robustness import RobustnessAnalyzer



def main():


    print()

    print(

        "ATLAS VALIDATION ENGINE"

    )

    print()



    # -------------------------------------------------
    # Create validator
    # -------------------------------------------------

    validator = WalkForwardValidator()



    # -------------------------------------------------
    # Run walk forward validation
    # -------------------------------------------------

    results = validator.run()



    # -------------------------------------------------
    # Validation report
    # -------------------------------------------------

    report = ValidationReport(

        results

    )


    report.display()



    # -------------------------------------------------
    # Robustness analysis
    # -------------------------------------------------

    robustness = RobustnessAnalyzer(

        results

    )


    robustness.display()





if __name__ == "__main__":

    main()