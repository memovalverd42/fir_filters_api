"""
This file contains the definitions of fir filter types.
"""
from typing import TypedDict


class FilterConf(TypedDict):
    """
    This class represents the configuration of a filter.
    """
    Ap: float
    """Passband ripple in dB"""

    As: float
    """Stopband attenuation in dB"""

    fp: float
    """Passband frequency in Hz"""

    fs: float
    """Stopband frequency in Hz"""

    F: float
    """Sampling frequency in Hz"""

    fs1: float | None
    """Stopband frequency 1 in Hz (optional)"""

    fp1: float | None
    """Passband frequency 1 in Hz (optional)"""

    fs2: float | None
    """Stopband frequency 2 in Hz (optional)"""

    fp2: float | None
    """Passband frequency 2 in Hz (optional)"""
