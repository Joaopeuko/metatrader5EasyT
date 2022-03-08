from unittest.mock import patch

import MetaTrader5

import metatrader5EasyT
from metatrader5EasyT.trade import Trade


class TestTrade:
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch('metatrader5EasyT.trade.Trade')
    def test_normalize(self, mock_tick_size, mock_symbol_info, mock_position_get):
        mock_symbol_info.return_value.trade_tick_size = 1e-05

        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        value_to_normalize = 12.3456789
        result = trade.normalize(value_to_normalize)
        assert result == 12.34

    @patch.object(MetaTrader5, 'symbol_info_tick')
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch.object(MetaTrader5, 'order_send')
    def test_open_buy(self, mock_order_send, mock_position_info, mock_position_get, mock_symbol_info_tick):
        mock_order_send.return_value.retcode = 10009
        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        trade.position_check()
        assert trade.trade_direction is None
        trade.open_buy()
        assert trade.trade_direction is 'buy'

    @patch.object(MetaTrader5, 'symbol_info_tick')
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch.object(MetaTrader5, 'order_send')
    def test_open_sell(self, mock_order_send, mock_position_info, mock_position_get, mock_symbol_info_tick):
        mock_order_send.return_value.retcode = 10009
        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        assert trade.trade_direction is None
        trade.open_sell()
        assert trade.trade_direction is 'sell'

    @patch.object(MetaTrader5, 'symbol_info_tick')
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch.object(Trade, 'position_open')
    @patch.object(MetaTrader5, 'order_send')
    def test_position_open(self, mock_order_send, mock_position_open, mock_position_info, mock_position_get, mock_symbol_info_tick):
        mock_order_send.return_value.retcode = [10009]
        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        trade._trade_allowed = True

        mock_position_open.return_value = 'buy'
        result = trade.position_open(buy=True, sell=False)
        assert result is 'buy'

        mock_position_open.return_value = 'sell'
        result = trade.position_open(False, True)
        assert result is 'sell'

        mock_position_open.return_value = None
        result = trade.position_open(False, False)
        assert result is None

        mock_position_open.return_value = None
        result = trade.position_open(True, True)
        assert result is None

    @patch.object(MetaTrader5, 'symbol_info_tick')
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch.object(MetaTrader5, 'order_send')
    @patch('metatrader5EasyT.trade.Trade')
    def test_position_close(self,mock_trade, mock_order_send, mock_symbol_info, mock_position_get,
                            mock_symbol_info_tick):
        mock_order_send.return_value.retcode = 10009
        mock_symbol_info.return_value.trade_tick_size = 1e-05
        mock_symbol_info_tick.return_value.ask = 1.00

        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        trade._trade_allowed = True

        trade.open_buy()
        assert trade.trade_direction is 'buy'

        mock_trade.return_value = None
        trade.position_close()
        assert trade.trade_direction is None

    @patch.object(MetaTrader5, 'symbol_info_tick')
    @patch.object(MetaTrader5, 'positions_get')
    @patch.object(MetaTrader5, 'symbol_info')
    @patch.object(MetaTrader5, 'order_send')
    @patch('metatrader5EasyT.trade.Trade')
    def test_position_check(self, mock_tick_size, mock_order_send, mock_trade, mock_position_get, mock_symbol_info_tick):
        mock_order_send.return_value.retcode = 10009
        mock_tick_size.return_value.points = 1e-05
        symbol = 'EURUSD'
        lot = 1.0
        stop_loss = 1.0
        take_profit = 1.0

        trade = Trade(symbol=symbol,
                      lot=lot,
                      stop_loss=stop_loss,
                      take_profit=take_profit)

        trade.open_buy()
        assert trade.trade_direction is 'buy'
        trade.position_close()
        assert trade.trade_direction is None
