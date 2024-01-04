from typing import Union
import functools
import time

import MetaTrader5 as _mt5

from .Errors import MT5Error
class MT5Wrappers:
    def load_mt5(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            _mt5.initialize()
            _mt5.login()
            result = fn(*args, **kwargs)
            _mt5.shutdown()
            return result
        return wrapper

    def load_symbol(fn):
        @functools.wraps(fn)
        def wrapper(data: Union[str, dict], *args, **kwargs):
            symbol = data["symbol"] if isinstance(data, dict) else data
            loaded = _mt5.symbol_select(symbol)
            if not loaded:
                raise MT5Error(f"Couldn't load {symbol}")
            result = fn(data, *args, **kwargs)
            # Tries to deselect it, if it can't it's fine
            _mt5.symbol_select(symbol, False)
            return result
        return wrapper