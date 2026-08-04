"""
Atlas AI Trading Platform 3.5

Walk Forward Validation Windows

Creates training and unseen validation
periods for robustness testing.
"""

from __future__ import annotations


from dataclasses import dataclass




# =====================================================
# WINDOW MODEL
# =====================================================

@dataclass(slots=True)
class ValidationWindow:


    training: object

    validation: object



    def __str__(self):

        return (

            f"Training candles: {len(self.training)} | "

            f"Validation candles: {len(self.validation)}"

        )





# =====================================================
# WINDOW GENERATOR
# =====================================================

class WindowGenerator:



    def __init__(

        self,

        training_size: int = 1000,

        validation_size: int = 250,

        step_size: int = 250,

        expanding: bool = True,

    ):


        self.training_size = training_size

        self.validation_size = validation_size

        self.step_size = step_size

        self.expanding = expanding





    # =====================================================
    # CREATE WINDOWS
    # =====================================================

    def generate(

        self,

        dataframe,

    ):


        windows = []



        if dataframe is None:

            print(
                "WINDOW ERROR: Dataset is None"
            )

            return windows



        total_rows = len(dataframe)



        print()

        print(
            f"Dataset candles available: {total_rows}"
        )

        print(
            f"Required per window: {self.training_size + self.validation_size}"
        )



        if total_rows < (

            self.training_size

            +

            self.validation_size

        ):


            print()

            print(
                "WINDOW ERROR: Not enough data"
            )

            return windows





        start = 0



        while True:



            if self.expanding:


                training_start = 0


            else:


                training_start = start




            training_end = (

                start

                +

                self.training_size

            )



            validation_end = (

                training_end

                +

                self.validation_size

            )



            if validation_end > total_rows:

                break





            training = dataframe.iloc[

                training_start:training_end

            ].copy()



            validation = dataframe.iloc[

                training_end:validation_end

            ].copy()




            if len(training) < self.training_size:

                break



            if len(validation) < self.validation_size:

                break





            windows.append(

                ValidationWindow(

                    training=training,

                    validation=validation,

                )

            )



            start += self.step_size





        print()

        print(

            f"Generated validation windows: {len(windows)}"

        )



        return windows