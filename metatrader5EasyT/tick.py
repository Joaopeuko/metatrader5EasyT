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

    def get_new_tick(self) -> None:
        """
        Everytime this function is called it update the last tick information, it is important to have update
        information know the most recent information.

        Returns:
             It updates the attributes in the constructor.
        """
        self._log.logger.info('Tick updated')
        result = Mt5.symbol_info_tick(self._symbol)

        self.time = result.time
        self.bid = result.bid
        self.ask = result.ask
        self.last = result.last
        self.volume = result.volume
