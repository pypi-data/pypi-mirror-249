from typing import Union, Optional
from pathlib import Path

from datetime import datetime
from datetime import timedelta


import shutil
import subprocess
import time
import logging
import sys

from Errors import MT5Error
from Global import TIMEFRAME

import MetaTrader5 as _mt5
from Decorators import MT5Wrappers as w

class MT5Utils:
    
    def normalize_path(self,
        path: Union[None, str, Path], 
        parent: Union[str, Path], 
        target: str
    ) -> str:
        """Takes a possible full path, partial path or None and
        turns it into the desired format."""
        parent = Path(parent)
        if path is None:
            return f"{str(parent.absolute())}{target}"
        else:
            path = Path(path)
            if path.is_dir():
                return f"{str(path.absolute())}{target}"
            else:
                return str(path.absolute())
    
    @w.load_mt5   
    def get_timzone_offset(self) -> float:
        """Function that calculated current timezone offset with broker server based on the difference
        between the last candle time and the current utc time in hours."""
        
        weekday = datetime.weekday(datetime.now())
        # if it is the weekend set the offset to 3 days
        if weekday in [4, 5, 6]:
            offset = 3 * 24 * 60 
        else:
            offset = 0 
            
        possible_symbols = _mt5.symbols_get()
        symbol = possible_symbols[0].name

        last_candle = _mt5.copy_rates_from_pos(symbol, TIMEFRAME.M1, offset, 1)
        last_candle_time = datetime.fromtimestamp(last_candle[0][0])
        reference = datetime.utcnow().replace(second=0, microsecond=0)
        reference -= timedelta(minutes=offset)
        offset = (last_candle_time - reference).total_seconds() / 3600

        return offset

