"""
Atlas AI Trading Platform 3.3

Walk Forward Window Generator

Creates:

Training Period
        |
Validation Period

Supports:

- Rolling windows
- Expanding windows
- Window numbering
"""

from __future__ import annotations


from dataclasses import dataclass

import pandas as pd



@dataclass
class ValidationWindow:


    window_id: int

    training: pd.DataFrame

    validation: pd.DataFrame



class WindowGenerator:


    def __init__(

        self,

        training_size: int = 500,

        validation_size: int = 100,

        step_size: int = 100,

        expanding: bool = True,

    ):


        self.training_size = training_size

        self.validation_size = validation_size

        self.step_size = step_size

        self.expanding = expanding



    # =====================================================
    # Generate Windows
    # =====================================================

    def generate(

        self,

        dataframe: pd.DataFrame,

    ) -> list[ValidationWindow]:


        windows = []


        start = 0

        window_number = 1



        while True:



            train_start = 0 if self.expanding else start


            train_end = (

                self.training_size + start

                if self.expanding

                else

                start + self.training_size

            )



            validation_start = train_end


            validation_end = (

                validation_start

                +

                self.validation_size

            )



            if validation_end > len(dataframe):

                break



            training = dataframe.iloc[

                train_start:train_end

            ].copy()



            validation = dataframe.iloc[

                validation_start:validation_end

            ].copy()



            windows.append(

                ValidationWindow(

                    window_id=window_number,

                    training=training,

                    validation=validation,

                )

            )



            window_number += 1


            start += self.step_size



        return windows