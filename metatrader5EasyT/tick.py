import MetaTrader5 as Mt5
from abstractEasyT import tick
from supportLibEasyT import log_manager


class Tick(tick.Tick):
    """
    Tick class is the responsible to retrieve every tick information.
    """
    def __init__(self,
                 symbol: str):
        """
        Args:
            symbol:
                It is the symbol you want information about. You can have information about time, bid, ask, last, volume.
        """

        self._log = log_manager.LogManager('metatrader5')
        self._log.logger.info('Logger Initialized in Tick')

        self._symbol = symbol.upper()

        self.time = None
        self.bid = None
        self.ask = None
        self.last = None
        self.volume = None

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

    def get_new_tick(self) -> None:
        """
        Everytime this function is called it update the last tick information, it is important to have update
        information know the most recent information.

        Returns:
             It updates the attributes in the constructor.

        Examples:
            >>> # All the code you need to execute the function:
            >>> from metatrader5EasyT.initialization import Initialize
            >>> from metatrader5EasyT.tick import Tick
            >>> initialize = Initialize()
            >>> initialize.initialize_platform()
            >>> initialize.initialize_symbol('EURUSD')
            >>> # It will return the most recent information, but it will return None at the first time.
            >>> # The tick need the information to be updated everytime.
            >>> eurusd_tick = Tick(symbol='EURUSD')
            >>> eurusd_tick.ask
            None
            >>> # When you update the tick:
            >>> eurusd_tick.get_new_tick()
            >>> eurusd_tick.ask
            1.09975
            >>> eurusd_tick.bid
            1.09975
            >>> # You must have notice that I used bid and ask, some exchanges do not return the last value
            >>> # You can find only the information for bid and ask. If you try to return last it will print 0.0.
            >>> # But remember, not all the exchanges do that, you must check it.
            >>> eurusd_tick.last
            0.0

            You can ask for this information: time, bid, ask, last, volume.

        """
        self._log.logger.info('Tick updated')
        result = Mt5.symbol_info_tick(self._symbol)

        self.time = result.time
        self.bid = result.bid
        self.ask = result.ask
        self.last = result.last
        self.volume = result.volume
