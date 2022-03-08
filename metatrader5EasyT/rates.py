import MetaTrader5 as Mt5
from abstractEasyT import rates
from supportLibEasyT import log_manager

from metatrader5EasyT.timeframe import TimeFrame


class Rates(rates.Rates):
    """
    This class is responsible to retrieve a certain amount of previous data.
    """
    def __init__(self,
                 symbol: str,
                 timeframe: TimeFrame,
                 count: int):
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

        self._log = log_manager.LogManager('metatrader5')
        self._log.logger.info('Logger Initialized in Rates')

        self._timeframe = timeframe
        self._symbol = symbol.upper()
        self._count = count

        self.time = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.tick_volume = None

    def update_rates(self) -> None:
        """
        Everytime this function is called it update the last values, it is important to have update information to
        calculate indicators and ensure your trading strategy is working properly.

        Returns:
            It updates the attributes in the constructor.
        """
        self._log.logger.info('Rates updated')
        result = Mt5.copy_rates_from_pos(self._symbol, self._timeframe, 0, self._count)

        self.time = result['time']
        self.open = result['open']
        self.high = result['high']
        self.low = result['low']
        self.close = result['close']
        self.tick_volume = result['tick_volume']
