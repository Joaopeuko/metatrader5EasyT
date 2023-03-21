import math

import MetaTrader5 as Mt5
from abstractEasyT import trade
from supportLibEasyT import log_manager


class Trade(trade.Trade):
    """
    This class is responsible to handle all the trade requests.
    """

    def __init__(self, symbol: str, lot: float, stop_loss: float, take_profit: float):
        """
        It is allowed to have only one position at time per symbol, right now it is not possible to open a position and
        increase the size of it or to open opposite position. Open an open position will close the other direction one.

        Args:
            symbol:
                It is the symbol you want to open or close or check if already have an operation opened.

            lot:
                It is how many shares you want to trade, many symbols allow fractions and others requires a
                certain amount. It can be 0.01, 100.0, 1000.0, 10000.0.

            stop_loss:
                It is how much you accept to lose. Example: If you buy a share for US$10.00, and you accept to lose US$1.00
                you set this variable at 1.00, you will be out of the operation at US$9.00 (sometimes more, somtime less,
                the US$9.00 is the trigger). Keep in mind that some symbols has different points metrics, US$1.00 sometimes
                can be 1000 points.

            take_profit:
                It is how much you accept to win. Example: If you buy a share for US$10.00, and you accept to win US$1.00
                you set this variable at 1.00, you will be out of the operation at US$11.00 (sometimes more, somtime less,
                the US$11.00 is the trigger). Keep in mind that some symbols has different points metrics, US$1.00 sometimes
                can be 1000 points.

        """

        self._log = log_manager.LogManager("metatrader5")
        self._log.logger.info("Logger Initialized in Trade")

        self.symbol = symbol.upper()
        self.lot = lot
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.ticket = None
        self.points = Mt5.symbol_info(self.symbol).trade_tick_size

        self._trade_allowed = False

        self.trade_direction = None  # 'buy', 'sell', or None for no position
        self.position_check()

    def normalize(self, price: float) -> float:
        """
        This function normalize the price to ensure a precision that is required by the platform

        Args:
            price:
                It is the price that you want to be normalized, usually is the last price to open a market position.

        Returns:
            It returns the float price normalized under a precision that is accepted by the platform.

        Examples:

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> # The normalize function is used inside other functions, but the idea is to normalize the value to
            >>> # be accepted in the trade request. If you want to see this function in action you can look at
            >>> # open_buy() and open_sell()
            >>> eurusd_trade.normalize(12.3456789)
            12.34

        """
        self._log.logger.info("Normalizing the price")
        return math.floor(float(self.points * round(price / self.points)) * 100) / 100

    def open_buy(self) -> None:
        """
        This functions when called send a buy request to Metatrader5 with the parameters in the attributes.

        Returns:
            It returns None, but if an error occurs when open a position it will break.

        Examples:

            Try this on your demo account with fake money, a position will be opened.

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            True
            2022-03-11 04:47:29,903 WARNING - initialize_platform - "Algotrading" not allowed! You cannot open position,
            but you can retrieve data. If you want to open positions, please, go to Metatrader5 and press the button
            "Algotrading."
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> # When I try to open a position and the Algotrading is not allowed on Metatrader5 I got a warning.
            >>> eurusd_trade.open_buy()
            2022-03-11 04:48:37,068 ERROR - open_buy - Something went wrong: Position Not Found for symbol EURUSD!
            Last Error: (1, 'Success')
            >>> # But when I allow algotrading, I return None, you can see at Metatrader5 that a buy
            position was opened.
            >>> eurusd_trade.open_buy()
            None
            >>> # Just for curiosity, if you want to try to open a sell position with this buy opened you will close
            >>> # the buy position
            >>> eurusd_trade.open_sell()
            None

        """
        price = Mt5.symbol_info_tick(self.symbol).ask

        self.ticket = (
            Mt5.positions_get(symbol=self.symbol)[0].ticket if len(Mt5.positions_get(symbol=self.symbol)) == 1 else 0
        )

        self._log.logger.info(
            f"BUY Order sent: {self.symbol},"
            f" {self.lot} lot(s),"
            f" at {price},"
            f" stoploss:{self.normalize(price - self.stop_loss)},"
            f" takeprofit: {self.normalize(price + self.take_profit)}."
        )

        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": Mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": self.normalize(price - self.stop_loss),
            "tp": self.normalize(price + self.take_profit),
            "deviation": 5,
            "magic": 7777,
            "comment": "easyT!",
            "type_time": Mt5.ORDER_TIME_GTC,
            "type_filling": Mt5.ORDER_FILLING_RETURN,
            "position": (
                Mt5.positions_get(symbol=self.symbol)[0].ticket
                if len(Mt5.positions_get(symbol=self.symbol)) == 1
                else 0
            ),
        }

        result = Mt5.order_send(request)

        if result is None or result.retcode != Mt5.TRADE_RETCODE_DONE:
            self._log.logger.error(
                f"Something went wrong: Position Not Found for symbol {self.symbol}!" f" Last Error: {Mt5.last_error()}"
            )

        else:
            self._log.logger.info("Change trade direction to BUY.")
            self.trade_direction = "buy"

    def open_sell(self):
        """
        This functions when called send a sell request to Metatrader5 with the parameters in the attributes.

        Returns:
            It returns None, but if an error occurs when open a position it will break.

        Examples:

            Try this on your demo account with fake money, a position will be opened.

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            True
            2022-03-11 04:47:29,903 WARNING - initialize_platform - "Algotrading" not allowed! You cannot open position,
            but you can retrieve data. If you want to open positions, please, go to Metatrader5 and press the button
            "Algotrading."
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> # When I try to open a position and the Algotrading is not allowed on Metatrader5 I got a warning.
            >>> eurusd_trade.open_sell()
            2022-03-11 04:57:08,628 ERROR - open_sell - Something went wrong: Position Not Found for symbol EURUSD!
            Last Error: (1, 'Success')
            >>> # But when I allow algotrading, I return None, you can see at Metatrader5 that a buy
            position was opened.
            >>> eurusd_trade.open_sell()
            None
            >>> # Just for curiosity, if you want to try to open a buy position with this sell opened you will close
            >>> # the sell position
            >>> eurusd_trade.open_buy()
            None

        """
        price = Mt5.symbol_info_tick(self.symbol).bid

        self.ticket = (
            Mt5.positions_get(symbol=self.symbol)[0].ticket if len(Mt5.positions_get(symbol=self.symbol)) == 1 else 0
        )

        self._log.logger.info(
            f"SELL Order sent: {self.symbol},"
            f" {self.lot} lot(s),"
            f" at {price},"
            f" stoploss:{self.normalize(price - self.stop_loss)},"
            f" takeprofit: {self.normalize(price + self.take_profit)}."
        )

        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": Mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": self.normalize(price + self.stop_loss),
            "tp": self.normalize(price - self.take_profit),
            "deviation": 5,
            "magic": 7777,
            "comment": "easyT",
            "type_time": Mt5.ORDER_TIME_GTC,
            "type_filling": Mt5.ORDER_FILLING_RETURN,
            "position": (
                Mt5.positions_get(symbol=self.symbol)[0].ticket
                if len(Mt5.positions_get(symbol=self.symbol)) == 1
                else 0
            ),
        }

        result = Mt5.order_send(request)
        if result is None or result.retcode != Mt5.TRADE_RETCODE_DONE:
            self._log.logger.error(
                f"Something went wrong: Position Not Found for symbol {self.symbol}!" f" Last Error: {Mt5.last_error()}"
            )

        else:
            self._log.logger.info("Change trade direction to SELL.")
            self.trade_direction = "sell"

    def position_open(self, buy: bool, sell: bool) -> str or None:
        """
        This function receives two bool variables, buy and sell, if one of this variable is true and the other is false,
        it opens a position to the side that is true, if both variable is true or both variable is false, it does not
        open a position.

        Args:
            buy:
                When buy is TRUE it receives a positive signal to open a position. When false, it is ignored.

            sell:
                When sell is TRUE it receives a positive signal to open a position. When false, it is ignored.

        Returns:
            It opens the position.

        Examples:

            Try this on your demo account with fake money, a position will be opened.

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            True
            2022-03-11 04:47:29,903 WARNING - initialize_platform - "Algotrading" not allowed! You cannot open position,
            but you can retrieve data. If you want to open positions, please, go to Metatrader5 and press the button
            "Algotrading."
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> # When I try to open a position and the Algotrading is not allowed on Metatrader5, return None'
            >>> eurusd_trade.position_open(True, False)
            None
            >>> # I allowed Algotrading, but when I try again, I receive None again.
            >>> eurusd_trade.position_open(True, False)
            None
            >>> # That behavior is happening because the attribute eurusd_trade._trade_allowed, is False as default.
            >>> eurusd_trade._trade_allowed
            False
            >>> # This attribute will be handled in another project, that is why it exists.
            >>> # Let assign to True and see what happens:
            >>> eurusd_trade._trade_allowed = True
            >>> eurusd_trade._trade_allowed
            True
            >>> # Let try to open a position.
            >>> eurusd_trade.position_open(True, False)
            'buy'
            >>> # It worked, lets try to double the position calling it again
            >>> eurusd_trade.position_open(True, False)
            'buy'
            >>> # The function returns 'buy', but another position was not opened, it returns the current trade
            >>> # direction
            >>> # I will call an opposite direction to see what happens:
            >>> eurusd_trade.position_open(False, True)
            'buy'
            >>> # The function returns 'buy', the position was not closed by trying to open another one in the opposite
            >>> # direction. No new position was opened, and it returns the current trade direction.
            >>> # I will close this position with eurusd_trade.position_close(), you can check what it does in the
            >>> # function documentation position_close()
            >>> eurusd_trade.position_close()
            None
            >>> # To finish, let see what happens if both arguments are True
            >>> eurusd_trade.position_open(True, True)
            None
            >>> # Nothing happens, but when both are False?
            >>> eurusd_trade.position_open(False, False)
            None
            >>> # Nothing happens

        """
        self._log.logger.info(
            f"Open position called. Buy is {str(buy)}, and sell is {str(sell)}. Trade allowed is "
            f"{self._trade_allowed}."
        )

        self.position_check()
        if self._trade_allowed and self.trade_direction is None:
            if buy and not sell:
                self._log.logger.info("BUY is true, SELL is false")
                self.open_buy()
                self.position_check()

            if sell and not buy:
                self._log.logger.info("BUY is false, SELL is true")
                self.open_sell()
                self.position_check()

        return self.trade_direction

    def position_close(self) -> None:
        """
        This functions checks the trade direction, and it opens an opposite position to the current one to close it.
        If there is no position nothing happens.

        Returns:
            Close the current position by opening an opposite one.

        Examples:

            Try this on your demo account with fake money, a position will be opened.

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            True
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> eurusd_trade._trade_allowed = True
            >>> # Opening a position with Algotrading allowed and, eurusd_trade._trade_allowed True
            >>> # To know more about eurusd_trade._trade_allowed look the Examples in position_open() documentation.
            >>> eurusd_trade.position_open(False, True)
            'sell'
            >>> # When there is a position opened, eurusd_trade.position_close() will open a position in a different
            >>> # direction to close it.
            >>> eurusd_trade.position_close()
            None
            # It checks the trading direction, return none when there is no trade opened.
            >>> eurusd_trade.trade_direction
            None
            # I will open a buy position, check the trade direction and close it!
            >>> eurusd_trade.position_open(True, False)
            'buy'
            >>>  eurusd_trade.trade_direction
            'buy'
            >>> eurusd_trade.position_close()
            >>> # We can see that it worked!
            >>> # What happens when I call eurusd_trade.position_close() with no position opened?
            >>> eurusd_trade.position_close()
            None
            >>> # Nothing happens, there are no position to be closed.


        """
        self._log.logger.info("Close position called.")
        self.position_check()
        if self.trade_direction == "buy":
            self._log.logger.info("Close BUY position.")
            self.open_sell()
            self.position_check()

        elif self.trade_direction == "sell":
            self._log.logger.info("Close SELL position")
            self.open_buy()
            self.position_check()

    def position_check(self) -> None:
        """
        This function checks if there are a position opened and update the variable self.trade_direction.
        If there is no position, the self.trade_direction will be updated to None, else, it updates with the trade
        direction, which can be 'sell' or 'buy'.

        Returns:
            This function update the variable self.trade_direction and do not return a result.

        Examples:

            Try this on your demo account with fake money, a position will be opened.

            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.trade import Trade
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            True
            >>> initialize.initialize_symbol('EURUSD')
            >>> eurusd_trade = Trade(symbol='EURUSD', lot=1.0, stop_loss=1.0, take_profit=1.0)
            >>> eurusd_trade._trade_allowed = True
            >>> # Position check it is just to ensure that the eurusd_trade.trade_direction are in the right direction.
            >>> # The eurusd_trade.trade_direction is automatically handled by buy open_sell() and open_buy() and
            >>> # it returns the trade direction or None when there is no trade opened.
            >>> eurusd_trade.trade_direction
            None
            >>> eurusd_trade.position_open(True, False)
            'buy'
            >>> eurusd_trade.trade_direction
            'buy'
            >>> # After I open a buy position, it returns 'buy' to trade_direction, but, what happens if I manually
            >>> # change the direction?
            >>> eurusd_trade.trade_direction = 'coffee shop'
            None
            >>> eurusd_trade.trade_direction
            'coffee shop'
            >>> # It is possible to see that the trade_direction was changed.
            >>> # and the position_check() is called in all the functions that opens and closes position
            >>> # to ensure that direction is correct, I will call position_check() to fix my change to 'coffee shop'
            >>> eurusd_trade.position_check()
            None
            >>> eurusd_trade.trade_direction
            'buy'
            >>> # It worked.
            >>> # That is it, I will just the position that I opened before.
            >>> eurusd_trade.position_close()


        """
        self._log.logger.info("Calls Metatrader5 to check if there is a position opened.")
        result = Mt5.positions_get(symbol=self.symbol)
        if len(result) > 0:
            self._log.logger.info("There is a position opened.")
            if result[0].type == 0:  # if buy
                self._log.logger.info("Set the trade direction to BUY")
                self.trade_direction = "buy"

            elif result[0].type == 1:  # if sell
                self._log.logger.info("Set the trade direction to SELL")
                self.trade_direction = "sell"
        else:
            self._log.logger.info("There are no position opened.")
            self._log.logger.info("Set the trade direction to None")
            self.trade_direction = None
