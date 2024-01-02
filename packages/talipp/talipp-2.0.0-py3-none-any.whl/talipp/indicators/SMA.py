from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType


class SMA(Indicator):
    """
    Simple Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if has_valid_values(self.input_values, self.period + 1):
            return self.output_values[-1] - \
                   (self.input_values[-self.period - 1] - self.input_values[-1]) / float(self.period)
        elif has_valid_values(self.input_values, self.period, exact=True):
            return float(sum(self.input_values[-self.period:])) / self.period
        else: # len(self.input_values) < self.period
            return None
