"""
Atlas AI Trading Platform

Alert Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod



class Alert(ABC):


    @abstractmethod
    def send(
        self,
        message: str,
    ):

        pass