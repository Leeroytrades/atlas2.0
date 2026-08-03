"""
Atlas AI Trading Platform 3.3

Base Strategy
"""

from __future__ import annotations


from abc import ABC, abstractmethod

import pandas as pd



class BaseStrategy(ABC):


    name = "BASE"


    supported_regimes = []



    def __init__(self):

        self.enabled = True



    @property
    def regimes(self):

        return self.supported_regimes



    def supports_regime(
        self,
        regime: str,
    ) -> bool:


        return (

            regime in self.supported_regimes

        )



    def info(self):

        return {

            "name": self.name,

            "regimes": self.supported_regimes,

            "enabled": self.enabled,

        }



    @abstractmethod
    def analyse(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        pass