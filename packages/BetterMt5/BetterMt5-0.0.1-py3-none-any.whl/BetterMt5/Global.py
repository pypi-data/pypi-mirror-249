import MetaTrader5 as mt5

class TIMEFRAME_SEC:
    """
    Timeframes in seconds given when requesting the simplified key of the MetaTrade5 lib. Eg. TIMEFRAME_SEC.M15 --> 900 (15 minutes in seconds)
    """
    M1 = 60
    M2 = 120
    M3 = 180
    M4 = 240
    M5 = 300
    M6 = 360
    M10 = 600
    M12 = 720
    M15 = 900
    M20 = 1200
    M30 = 1800
    H1 = 3600
    H2 = 7200
    H3 = 10800
    H4 = 14400
    H6 = 21600
    H8 = 28800
    H12 = 43200
    D1 = 86400
    W1 = 604800
    MN1 = 2592000


class TIMEFRAME:
    """
    Timeframes of the MetaTrade5 lib. Eg. TIMEFRAME.M15 --> MetaTrader5.TIMEFRAME_M15
    """
    M1 = mt5.TIMEFRAME_M1
    M2 = mt5.TIMEFRAME_M2
    M3 = mt5.TIMEFRAME_M3
    M4 = mt5.TIMEFRAME_M4
    M5 = mt5.TIMEFRAME_M5
    M6 = mt5.TIMEFRAME_M6
    M10 = mt5.TIMEFRAME_M10
    M12 = mt5.TIMEFRAME_M12
    M15 = mt5.TIMEFRAME_M15
    M20 = mt5.TIMEFRAME_M20
    M30 = mt5.TIMEFRAME_M30
    H1 = mt5.TIMEFRAME_H1
    H2 = mt5.TIMEFRAME_H2
    H3 = mt5.TIMEFRAME_H3
    H4 = mt5.TIMEFRAME_H4
    H6 = mt5.TIMEFRAME_H6
    H8 = mt5.TIMEFRAME_H8
    H12 = mt5.TIMEFRAME_H12
    D1 = mt5.TIMEFRAME_D1
    W1 = mt5.TIMEFRAME_W1
    MN1 = mt5.TIMEFRAME_MN1

class ORDER_TYPES:
    BUY = mt5.ORDER_TYPE_BUY
    SELL = mt5.ORDER_TYPE_SELL
    BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    SELL_STOP = mt5.ORDER_TYPE_SELL_STOP
    BUY_STOP_LIMIT = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    SELL_STOP_LIMIT = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    CLOSE = mt5.ORDER_TYPE_CLOSE_BY
