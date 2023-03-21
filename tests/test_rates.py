from unittest.mock import patch

import MetaTrader5

from metatrader5EasyT.rates import Rates
from metatrader5EasyT.timeframe import TimeFrame


class TestRates:
    def test_rates_created_but_not_updated(self):
        symbol = "EURUSD"
        count = 20
        timeframe = TimeFrame()

        rates = Rates(symbol=symbol, timeframe=timeframe.ONE_MINUTE, count=count)

        assert rates.time is None
        assert rates.open is None
        assert rates.high is None
        assert rates.low is None
        assert rates.close is None
        assert rates.tick_volume is None

    @patch.object(
        MetaTrader5,
        "copy_rates_from_pos",
        return_value={
            "time": range(20),
            "open": range(20),
            "high": range(20),
            "low": range(20),
            "close": range(20),
            "tick_volume": range(20),
        },
    )
    def test_length(self, mock):
        symbol = "EURUSD"
        count = 20
        timeframe = TimeFrame()

        rates = Rates(symbol=symbol, timeframe=timeframe.ONE_MINUTE, count=count)

        rates.update_rates()

        assert len(rates.time) == 20
        assert len(rates.open) == 20
        assert len(rates.high) == 20
        assert len(rates.low) == 20
        assert len(rates.close) == 20
        assert len(rates.tick_volume) == 20
