import pytest
import MetaTrader5

from unittest.mock import patch, PropertyMock

from metatrader5EasyT.initialization import Initialize
from metatrader5EasyT.initialization import SymbolNotFound
from metatrader5EasyT.initialization import PlatformNotInitialized


class TestInitialization:
    # ------------------------------ Platform ------------------------------ #
    @patch('tests.test_initialization.Initialize', side_effect=PlatformNotInitialized)
    def test_initialize_platform_fail_raises(self, mock):
        with pytest.raises(PlatformNotInitialized):
            Initialize().initialize_platform()

    @patch.object(MetaTrader5, 'initialize', return_value=False)
    def test_initialize_platform_fail_false(self, mock):
        with pytest.raises(PlatformNotInitialized):
            Initialize().initialize_platform()

    @patch.object(MetaTrader5, 'terminal_info')
    @patch.object(MetaTrader5, 'initialize', return_value=True)
    def test_initialize_platform_succeed(self, mock_trade_allowed, mock):
        result = Initialize().initialize_platform()
        assert result is True

    # ------------------------------ Symbol ------------------------------ #

    @patch.object(MetaTrader5, 'symbol_info', return_value=True)
    def test_initialize_symbol_succeed(self, mock):
        symbol = 'EURUSD'

        result = Initialize().initialize_symbol(symbol)
        assert result is True

    @patch.object(MetaTrader5, 'symbol_info', return_value=True)
    def test_initialize_symbol_succeed_lower(self, mock):
        symbol = 'eurusd'

        result = Initialize().initialize_symbol(symbol)
        assert result is True

    @patch('tests.test_initialization.Initialize', side_effect=SymbolNotFound)
    def test_initialize_symbol_fail(self, mock):
        symbol = 'eur usd'

        with pytest.raises(SymbolNotFound):
            Initialize().initialize_symbol(symbol)
