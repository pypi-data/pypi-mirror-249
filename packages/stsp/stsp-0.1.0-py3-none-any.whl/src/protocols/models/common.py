import typing as tp
from datetime import datetime
from decimal import Decimal as Dec


class OHLC(tp.TypedDict):
    date_time: datetime
    open: Dec
    high: Dec
    low: Dec
    close: Dec
    volume: int
