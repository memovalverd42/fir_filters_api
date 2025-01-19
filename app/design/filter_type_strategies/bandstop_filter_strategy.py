"""
This file contains the implementation of the bandstop filter strategy.
"""
import math

from app.design.filter_type_strategies.filter_type_strategy import FilterTypeStrategy
from app.design.types.fir_filter_types import FilterConf
from app.design.validators.filter_conf_validator import FilterConfValidator


class BandStopFilterStrategy(FilterTypeStrategy, FilterConfValidator):
    """
    The BandStop Filter Strategy class implements the Filter Type Strategy interface.
    """

    def __init__(self, filter_conf: FilterConf, round_value: int = 7):

        FilterConfValidator.__init__(self, filter_conf)

        self.round_value = round_value

        self.F = filter_conf['F']

        # TODO: Validate if these values are correct
        self.fp1 = filter_conf['fp1']
        self.fs1 = filter_conf['fs1']

        self.fp2 = filter_conf['fp2']
        self.fs2 = filter_conf['fs2']

        self.n = None

    def calculate_filter_order(self, d: float) -> tuple[int, float, int]:
        if d == 0:
            raise ValueError("d cannot be 0")

        N = round(((self.F * d) / (min(self.fs1 - self.fp1, self.fp2 - self.fs2))) + 1, self.round_value)

        N_o = N

        N_int = int(N)
        if (N_int + 1) % 2 == 0:
            N = N_int + 2
        else:
            N = N_int + 1

        self.n = int((N - 1) / 2)

        return N, N_o, self.n

    def get_impulse_response(self) -> list[float]:
        coef = []
        nc = 1

        deltaF = min(self.fs1 - self.fp1, self.fp2 - self.fs2)
        fc1 = self.fp1 + (deltaF / 2)
        fc2 = self.fp2 - (deltaF / 2)

        n0 = (2 / self.F) * (fc1 - fc2) + 1
        coef.append(n0)

        while nc <= self.n:
            term1 = (2 * math.pi * nc * fc1) / self.F
            term2 = (2 * math.pi * nc * fc2) / self.F
            c = (1 / (nc * math.pi)) * ((math.sin(term1)) - (math.sin(term2)))
            nc = nc + 1
            coef.append(round(c, self.round_value))

        return coef
