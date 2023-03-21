import MetaTrader5 as Mt5
from abstractEasyT import timeframe
from supportLibEasyT import log_manager


class TimeFrame(timeframe.TimeFrame):
    """
    There are incompatibilities and different patterns in writing the timeframe between platforms.
    This class attend to reduce the chance of errors providing the same timeframe structure between platforms.

    Examples:
        You can find an example of the TimeFrame usage in update_rates() function in Rates documentation
    """

    def __init__(self):
        self._log = log_manager.LogManager("metatrader5")
        self._log.logger.info("Logger Initialized in TimeFrame")

        self.ONE_MINUTE = Mt5.TIMEFRAME_M1  # 1 minute
        self.TWO_MINUTES = Mt5.TIMEFRAME_M2  # 2 minutes
        self.THREE_MINUTES = Mt5.TIMEFRAME_M3  # 3 minutes
        self.FOUR_MINUTES = Mt5.TIMEFRAME_M4  # 4 minutes
        self.FIVE_MINUTES = Mt5.TIMEFRAME_M5  # 5 minutes
        self.SIX_MINUTES = Mt5.TIMEFRAME_M6  # 6 minutes
        self.TEN_MINUTES = Mt5.TIMEFRAME_M10  # 10 minutes
        self.TWELVE_MINUTES = Mt5.TIMEFRAME_M12  # 12 minutes
        self.FIFTEEN_MINUTES = Mt5.TIMEFRAME_M15  # 15 minutes
        self.TWENTY_MINUTES = Mt5.TIMEFRAME_M20  # 20 minutes
        self.THIRTY_MINUTES = Mt5.TIMEFRAME_M30  # 30 minutes
        self.ONE_HOUR = Mt5.TIMEFRAME_H1  # 1 hour
        self.TWO_HOURS = Mt5.TIMEFRAME_H2  # 2 hour
        self.THREE_HOURS = Mt5.TIMEFRAME_H3  # 3 hour
        self.FOUR_HOURS = Mt5.TIMEFRAME_H4  # 4 hour
        self.SIX_HOURS = Mt5.TIMEFRAME_H6  # 6 hour
        self.EIGHT_HOURS = Mt5.TIMEFRAME_H8  # 8 hour
        self.TWELVE_HOURS = Mt5.TIMEFRAME_H12  # 12 hour
        self.ONE_DAY = Mt5.TIMEFRAME_D1  # 1 Day
        self.THREE_DAY = None  # 3 Days
        self.ONE_WEEK = Mt5.TIMEFRAME_W1  # 1 Week
        self.ONE_MONTH = Mt5.TIMEFRAME_MN1  # 1 Month
