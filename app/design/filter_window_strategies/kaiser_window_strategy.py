"""
This file contains the implementation of the Kaiser window strategy.
"""
import math

from app.design.filter_window_strategies.filter_window_strategy import FilterWindowStrategy


class KaiserWindowStrategy(FilterWindowStrategy):
    """
    The Kaiser Window Strategy class implements the Filter Window Strategy interface.
    """

    def __init__(self, round_value: int = 7):
        self.round_value = round_value

        self.alpha = None
        self.betas = None

    def _calculate_alpha_parameter(self, AS: float) -> float:
        """
        This method calculates the alpha parameter for the Kaiser window.
        :param AS: Stopband attenuation
        """
        if AS <= 21:
            self.alpha = 0
        elif 21 < AS <= 50:
            self.alpha = round(
                (0.5842 * (AS - 21) ** 0.4) + 0.07886 * (AS - 21),
                self.round_value
            )
        else:
            self.alpha = round(0.1102 * (AS - 8.7), self.round_value)

        return self.alpha

    def _calculate_betas(self, n: int, n_factor: int) -> list[float]:
        """
        This method calculates the beta values for the Kaiser window.
        :param n: Filter Order
        :param n_factor: Factor to calculate N
        """
        betas = []
        nc = 0

        while nc <= n:
            b = self.alpha * (1 - ((2 * nc) / (n_factor - 1)) ** 2) ** 0.5
            betas.append(round(b, self.round_value))
            nc = nc + 1

        self.betas = betas
        return self.betas

    def _sum_k_coefficients(self, factor: float) -> float:
        """
        This method calculates the sum of the coefficients of the Kaiser window.
        :param factor: Factor to calculate the sum
        """
        k = 1
        result = 0
        while k <= 25:
            sum = ((1 / math.factorial(k)) * (factor / 2) ** k) ** 2
            result = result + round(sum, self.round_value)
            k = k + 1

        return result + 1

    def calculate_window_coeficients(self, n: int, n_factor: int, AS: float) -> list[float]:
        if not self.alpha:
            raise ValueError("Alpha parameter not calculated")

        if not self.betas:
            raise ValueError("Betas not calculated")

        # Calculate alpha
        self._calculate_alpha_parameter(AS=AS)

        # Calculate betas
        self._calculate_betas(n=n, n_factor=n_factor)

        coef_k = []

        I_alpha = self._sum_k_coefficients(self.alpha)
        for beta in self.betas:
            coef = self._sum_k_coefficients(beta) / I_alpha
            coef_k.append(round(coef, self.round_value))

        return coef_k
