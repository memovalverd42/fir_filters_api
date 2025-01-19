"""
This file contains the interface of the Filter Type Strategy.
"""
from abc import ABC, abstractmethod


class FilterTypeStrategy(ABC):
    """
    The Filter Type Strategy interface declares operations common.
    """

    @abstractmethod
    def calculate_filter_order(self, d: float) -> tuple[int, int, int]:
        """
        This method calculates the filter order (N).
        """
        pass

    @abstractmethod
    def get_impulse_response(self) -> list[float]:
        """
        This method calculates the impulse response of the filter.
        """
        pass
