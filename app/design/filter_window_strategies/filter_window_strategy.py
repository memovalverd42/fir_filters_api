"""
This file contains the Filter Window Strategy interface.
"""
from abc import ABC, abstractmethod


class FilterWindowStrategy(ABC):
    """
    The Filter Window Strategy interface declares operations common.
    """

    @abstractmethod
    def calculate_window_coeficients(self, n: int, n_factor: int) -> list[float]:
        """
        This method calculates the window coefficients.
        :param n: Filter Order
        :param n_factor: Factor to calculate N
        :return: List of window coefficients
        """
        pass
