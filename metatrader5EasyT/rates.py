import MetaTrader5 as Mt5
from abstractEasyT import rates
from supportLibEasyT import log_manager

from metatrader5EasyT.timeframe import TimeFrame


class Rates(rates.Rates):
    """
    This class is responsible to retrieve a certain amount of previous data.
    """

    def __init__(self, symbol: str, timeframe: TimeFrame, count: int):
        """
        Args:
            symbol:
                The symbol you want to retrieve previous data.

            timeframe:
                The timeframe you want information, like 1 minute, 5 minute, 1 week. You can find all the timeframe
                available in the TimeFrame Class (metatrader5EasyT.timeframe).

            count:
                It is the amount of information in the past you want. If your time frame is 5 minutes and your count is 4,
                it will return 4 values containing time, open, high, low, close, tick_volume information of this past 4
                candlesticks.
        """

        self._log = log_manager.LogManager("metatrader5")
        self._log.logger.info("Logger Initialized in Rates")

        self._timeframe = timeframe
        self._symbol = symbol.upper()
        self._count = count

        self.time = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.tick_volume = None

    def change_symbol(self, new_symbol: str) -> None:
        """
        This function changes the symbol.

        Args:
            new_symbol:
                It receives the new symbol

        Returns:
            It updates the self._symbol to the new symbol.

        """
        self._symbol = new_symbol.upper()

    def change_timeframe(self, new_timeframe: TimeFrame) -> None:
        """
        This function changes the timeframe.

        Args:
            new_timeframe:
                It receives the new timeframe

        Returns:
            It updates the self._timeframe to the new timeframe.

        """
        self._timeframe = new_timeframe

    def change_count(self, new_count: int) -> None:
        """
        This function changes the count.

        Args:
            new_count:
                It receives the new new_count

        Returns:
            It updates the self._count to the new count.

        Examples:
            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.timeframe import TimeFrame
            >>> from metatrader5EasyT.rates import Rates
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            >>> initialize.initialize_symbol('EURUSD')
            >>> timeframe = TimeFrame()
            >>> # it will get the last 20 one minute candlestick information.
            >>> eurusd_rates = Rates(symbol='EURUSD', timeframe=timeframe.ONE_MINUTE, count=20)
            >>> eurusd_rates.update_rates()
            >>> len(eurusd_rates.close)
            20
            >>> # When you change the count, you need to update the information, and you can see that it worked.
            >>> eurusd_rates.change_count(5)
            >>> eurusd_rates.update_rates()
            >>> len(eurusd_rates.close)
            5

            You can ask for this information: time, open, high, low, close, tick_volume.

        """
        self._count = new_count

    def update_rates(self) -> None:
        """
        Everytime this function is called it update the last values, it is important to have update information to
        calculate indicators and ensure your trading strategy is working properly.

        Returns:
            It updates the attributes in the constructor.

        Examples:
            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.timeframe import TimeFrame
            >>> from metatrader5EasyT.rates import Rates
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            >>> timeframe = TimeFrame()
            >>> initialize.initialize_symbol('EURUSD')
            >>> # it will get the last 20 one minute candlestick information, but it will return none at the first time.
            >>> # the rates need the information to be updated everytime.
            >>> eurusd_rates = Rates(symbol='EURUSD', timeframe=timeframe.ONE_MINUTE, count=20)
            >>> # The first time, if you try to get a rates information of the close price you will receive None
            >>> eurusd_rates.close
            None
            >>> # But when you update the rates, the prices will be updated.
            >>> eurusd_rates.update_rates()
            >>> # And the rates will be returned for the information you want.
            >>> eurusd_rates.close
            array([1.10324, 1.10342, 1.10329, 1.10338, 1.10294, 1.10238, 1.10188,
            1.10186, 1.10221, 1.10172, 1.1013 , 1.10069, 1.10097, 1.10104,
            1.10081, 1.1003 , 1.10036, 1.10147, 1.10068, 1.10072])

            You can ask for this information: time, open, high, low, close, tick_volume.

        """

        self._log.logger.info("Rates updated")
        result = Mt5.copy_rates_from_pos(self._symbol, self._timeframe, 0, self._count)

        self.time = result["time"]
        self.open = result["open"]
        self.high = result["high"]
        self.low = result["low"]
        self.close = result["close"]
        self.tick_volume = result["tick_volume"]
