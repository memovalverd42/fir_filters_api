"""
Main file
"""
from app.design.filter_type_strategies.highpass_filter_strategy import HighPassFilterStrategy
from app.design.filter_window_strategies.hamming_window_strategy import HammingWindowStrategy
from app.design.fir_filter import FIRFilter
from app.design.types.fir_filter_types import FilterConf

hp_hamming_conf = FilterConf(
    Ap=0.4,
    As=34,
    fp=16,
    fs=8,
    F=80,
)


filter_strategy = HighPassFilterStrategy(hp_hamming_conf)
window_strategy = HammingWindowStrategy()

hp_hamming = FIRFilter(
    filter_conf=hp_hamming_conf,
    filter_strategy=filter_strategy,
    window_strategy=window_strategy
)


hp_hamming.execute()
