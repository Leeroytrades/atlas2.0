"""
Atlas AI Trading Platform

Broker Base Interface

All broker implementations must follow this contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Broker(ABC):
    """
    Abstract broker interface.
    """


    @abstractmethod
    def submit_order(
        self,
        trade,
    ):
        """
        Submit a trade order.
        """

        pass


    @abstractmethod
    def close_order(
        self,
        trade,
        exit_price: float,
    ):
        """
        Close an existing trade.
        """

        pass


    @abstractmethod
    def get_positions(self):
        """
        Return current positions.
        """

        pass


    @abstractmethod
    def get_account(self):
        """
        Return account information.
        """

        pass