import MetaTrader5 as Mt5
from supportLibEasyT import log_manager
from abstractEasyT import initialization


class PlatformNotInitialized(BaseException):
    """Raise this error when the Metatrader5 is not installed or not possible to load it for some reason."""


class SymbolNotFound(BaseException):
    """Raise this error when the symbol is not found."""


class Initialize(initialization.Initialize):
    """
    This class ensure that the platform are working properly.
    If it is connected on the internet, and if the symbol that you are trying to use exists or was not mistyped.
    """

    def __init__(self):
        """
        Initialize the constructor and set the _log.
        """

        self._log = log_manager.LogManager('metatrader5')
        self._log.logger.info('Logger Initialized in Initialize')

        self.symbol_initialized = []

    def initialize_platform(self) -> bool:
        """
        This function is responsible to initialize the platform that will be used to trade.

        Raises:
            PlatformNotInitialized: Raise this error when the Metatrader5 is not installed or not possible to load
            it for some reason.

        Returns:
            It returns true if initialized else return false.
        """
        self._log.logger.info('Initializing Metatrader5.')
        initialization_result = Mt5.initialize()
        if not initialization_result:
            self._log.logger.error('Initialization failed, check internet connection.'
                                   ' You must have MetaTrader5 installed on Windows.')

            raise PlatformNotInitialized

        else:
            self._log.logger.info('Metatrader5 successfully initialized.')

        if not Mt5.terminal_info().trade_allowed:
            self._log.logger.warning('"Algotrading" not allowed! You cannot open position, but you can retrieve data.'
                                     ' If you want to open positions, please, go to Metatrader5 and press the button'
                                     ' "Algotrading."')

        return initialization_result

    def initialize_symbol(self, *symbols: str) -> bool:
        """
        This function is responsible to initialize as many symbols as you want.

        Args:
            symbols:
                It receives strings as parameters containing the symbol names to be initialized.

        Raises:
            SymbolNotFound: If not possible to initialize the symbol raises this error.

        Returns:
            When the symbol is successfully initialized it returns True and, it updates the list
            self.symbol_initialized if you want to work with the symbols correctly initialized.
        """
        self._log.logger.info('Initializing symbols.')
        for symbol in symbols:
            symbol = symbol.upper()
            self._log.logger.info(f'Initializing {symbol}.')
            Mt5.symbol_select(symbol, True)

            # Prepare the symbol to open positions
            symbol_info = Mt5.symbol_info(symbol)
            if symbol_info is None:
                self._log.logger.error(f'It was not possible to initialize {symbol}, symbol not found or not visible.')
                raise SymbolNotFound

            else:
                self.symbol_initialized.append(symbol)
                self._log.logger.info(f'{symbol} successfully initialized.')
                return True
