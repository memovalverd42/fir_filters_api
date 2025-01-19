"""
This file contains the implementation of the filter class
"""
import math
import numpy as np
from scipy.signal import freqz
import matplotlib.pyplot as plt
from tabulate import tabulate

from app.design.filter_type_strategies.filter_type_strategy import FilterTypeStrategy
from app.design.filter_window_strategies.filter_window_strategy import FilterWindowStrategy
from app.design.types.fir_filter_types import FilterConf


def show_coef_table(coefficients: list[float]):
    n = len(coefficients)
    data = [
        [i+1, value]
        for i, value in enumerate(coefficients)
    ]
    headers = ['n', 'value']

    return (
        tabulate(data, headers=headers, tablefmt="fancy_grid")
    )


class FIRFilter:
    """
    FIR Filter class
    """
    delta = 0
    AS = 0
    AP = 0
    D = 0
    alpha = 0

    def __init__(
            self,
            filter_conf: FilterConf,
            filter_strategy: FilterTypeStrategy,
            window_strategy: FilterWindowStrategy,
            round_value: int = 7

    ):
        self.filter_conf = filter_conf
        self.round_value = round_value
        self.filter_strategy = filter_strategy
        self.window_strategy = window_strategy

        self.As = filter_conf['As']
        self.Ap = filter_conf['Ap']
        self.fp = filter_conf['fp']
        self.fs = filter_conf['fs']
        self.F = filter_conf['F']

    def _calculate_delta(self) -> float:
        """
        Calculates the delta parameter for the filter
        :return: Delta Value Calculated
        """
        delta_s = 10 ** (-0.05 * self.As)
        delta_p = (10 ** (0.05 * self.Ap) - 1) / (10 ** (0.05 * self.Ap) + 1)
        self.delta = round(min(delta_s, delta_p), self.round_value)
        return self.delta

    def _calculate_ripples(self) -> tuple[float, float]:
        """
        Calculate de ripple values
        :return: tuple with As and Ap values respectively
        """
        self.AS = round(-20 * math.log10(self.delta), self.round_value)
        self.AP = round(20 * math.log10((1 + self.delta) / (1 - self.delta)), self.round_value)
        return self.AS, self.AP

    def _calculate_d_parameter(self) -> float:
        """
        Calculetes the D parameter for the filter
        """
        if self.AS <= 21:
            self.D = 0.9222
        else:
            self.D = round((self.AS - 7.95) / 14.36, self.round_value)

        return self.D

    def _calculate_alpha_parameter(self):
        if self.AS <= 21:
            self.alpha = 0
        elif 21 < self.AS <= 50:
            self.alpha = round(
                (0.5842 * (self.AS - 21) ** 0.4) + 0.07886 * (self.AS - 21),
                self.round_value
            )
        else:
            self.alpha = round(0.1102 * (self.AS - 8.7), self.round_value)

    @staticmethod
    def order_coefficients(coefficients: list[float]):
        """
        Order coefficients for graffic
        :param coefficients:
        """
        idx = len(coefficients) - 1
        cont = 1
        coef_ordered = []
        while idx >= 0:
            if coefficients[idx] == -0.0 or coefficients[idx] == 0.0:
                cero = int(np.abs(coefficients[idx]))
                coef_ordered.append(cero)
            else:
                coef_ordered.append(coefficients[idx])
            idx = idx - 1

        while cont <= (len(coefficients) - 1):
            if coefficients[cont] == -0.0 or coefficients[cont] == 0.0:
                cero = int(np.abs(coefficients[cont]))
                coef_ordered.append(cero)
            else:
                coef_ordered.append(coefficients[cont])
            cont = cont + 1

        return coef_ordered

    def plot(self, coefficients: list[float]):
        """
        Plots the filter graphic
        :param coefficients:
        """
        num = coefficients
        den = 1

        w, h = freqz(num, den, 100)

        hertz = w * self.F / (2 * np.pi)

        plt.semilogy(hertz, np.abs(h))
        plt.grid()
        plt.show()

    def execute(self):
        """
        Executes the creation of the filter
        """
        # Delta
        self._calculate_delta()
        # AS and AP
        self._calculate_ripples()
        # D Parameter
        self._calculate_d_parameter()
        # Alpha
        self._calculate_alpha_parameter()
        # Filter order
        N, N_o, n = self.filter_strategy.calculate_filter_order(self.D)
        # Coefficients
        coefficients = self.filter_strategy.get_impulse_response()
        # Window
        window_coef = self.window_strategy.calculate_window_coeficients(n, N)

        coef_filt = []

        for i in range(n + 1):
            coef_filt.append(round(window_coef[i] * coefficients[i], self.round_value))

        coef_filt_ordenados = self.order_coefficients(coef_filt)

        print(show_coef_table(coef_filt_ordenados))

        self.plot(coef_filt_ordenados)


