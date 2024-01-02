from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAType, MAFactory


class MeanDev(Indicator):
    """
    Mean Deviation

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None, ma_type: MAType = MAType.SMA):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.ma = MAFactory.get_ma(ma_type, period)
        self.add_sub_indicator(self.ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ma, 1):
            return None

        return sum(map(lambda x: abs(x - self.ma[-1]), self.input_values[-self.period:])) / float(self.period)
