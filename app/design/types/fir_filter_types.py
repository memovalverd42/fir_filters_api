"""
This file contains the definitions of fir filter types.
"""
from typing import TypedDict, Literal

FilterType = Literal['passband', 'lowpass', 'highpass', 'bandpass']
FilterWindow = Literal['hamming', 'blackman', 'kaiser']

class FilterConf(TypedDict):
    """
    This class represents the configuration of a filter.
    """
    filter_type: FilterType
    """Filter type"""

    filter_window: FilterWindow
    """Filter window"""

    Ap: float
    """Passband ripple in dB"""

    As: float
    """Stopband attenuation in dB"""

    fp: float
    """Passband frequency in Hz (pole frequency 1)"""

    fs: float
    """Stopband frequency in Hz (zero frequency 1)"""

    F: float
    """Sampling frequency in Hz"""

    fs2: float | None
    """Stopband frequency 2 in Hz (optional - pole frequency 2)"""

    fp2: float | None
    """Passband frequency 2 in Hz (optional - zero frequency 2)"""
