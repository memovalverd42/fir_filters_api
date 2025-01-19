"""
This file contains the Lowpass Filter Strategy implementation.
"""
import math

from app.design.filter_type_strategies.filter_type_strategy import FilterTypeStrategy
from app.design.types.fir_filter_types import FilterConf
from app.design.validators.filter_conf_validator import FilterConfValidator


class LowPassFilterStrategy(FilterTypeStrategy, FilterConfValidator):
    """
    The Lowpass Filter Strategy class implements the Filter Type Strategy interface.
    """
    FILTER_ORDER_FACTOR = 2

    def __init__(self, filter_conf: FilterConf, round_value: int = 7):

        FilterConfValidator.__init__(self, filter_conf)

        self.round_value = round_value

        self.F = filter_conf['F']
        self.fp = filter_conf['fp']
        self.fs = filter_conf['fs']

        self.n = None

    def calculate_filter_order(self, d: float) -> tuple[int, int, int]:
        if d == 0:
            raise ValueError("d cannot be 0")
        N = int(((self.F * d) / (self.fs - self.fp)) + self.FILTER_ORDER_FACTOR)

        N_o = N

        N_int = int(N)
        if (N_int + 1) % 2 == 0:
            N = N_int + 2
        else:
            N = N_int + 1

        self.n = int((N - 1) / 2)

        return N, N_o, self.n

    def get_impulse_response(self) -> list[float]:
        if not self.n:
            raise ValueError("Filter order is not defined")

        coef = []
        nc = 1
        fc = 0.5 * (self.fp + self.fs)
        n0 = (2 * fc) / self.F
        coef.append(n0)

        while nc <= self.n:
            term = (2 * math.pi * nc * fc) / self.F
            c = n0 * ((math.sin(term)) / term)
            nc = nc + 1
            coef.append(round(c, self.round_value))

        return coef

    def get_filter_window_coeficients(self):
        pass
