"""
This file contains the implementation of the Blackman window strategy.
"""
import math

from app.design.filter_window_strategies.filter_window_strategy import FilterWindowStrategy


class BlackmanWindowStrategy(FilterWindowStrategy):
    """
    The Blackman Window Strategy class implements the Filter Window Strategy interface.
    """

    def __init__(self, round_value: int = 7):
        self.round_value = round_value

    def calculate_window_coeficients(self, n: int, n_factor: int) -> list[float]:
        nc = 0
        coef = []
        while nc <= n:
            r = (
                    0.42 + 0.5 * math.cos((2 * math.pi * nc) / (n_factor - 1)) + 0.08 * math.cos((4 * math.pi * nc) / (n_factor - 1))
            )
            nc = nc + 1
            coef.append(round(r, self.round_value))

        return coef