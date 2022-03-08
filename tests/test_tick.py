import MetaTrader5

from unittest.mock import patch

from metatrader5EasyT.tick import Tick


class TestTick:

    def test_tick_created_but_not_updated(self):
        symbol = 'EURUSD'

        tick = Tick(symbol=symbol)

        assert tick.time is None
        assert tick.bid is None
        assert tick.ask is None
        assert tick.last is None
        assert tick.volume is None

    @patch.object(MetaTrader5, 'symbol_info_tick')
    def test_type(self, mock_tick):
        mock_tick.return_value.time = 1
        mock_tick.return_value.bid = 1.0
        mock_tick.return_value.ask = 1.0
        mock_tick.return_value.last = 1.0
        mock_tick.return_value.volume = 1

        symbol = 'EURUSD'

        tick = Tick(symbol=symbol)

        tick.get_new_tick()

        assert type(tick.time) == int
        assert type(tick.bid) == float
        assert type(tick.ask) == float
        assert type(tick.last) == float
        assert type(tick.volume) == int
