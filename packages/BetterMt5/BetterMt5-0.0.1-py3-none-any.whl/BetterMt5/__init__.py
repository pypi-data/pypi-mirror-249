import MetaTrader5 as mt5
from .BMT5Utils import MT5Utils

class BetterMt5():
    def __init__(self) -> None:
        self.util = MT5Utils()