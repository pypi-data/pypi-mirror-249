import typing as tp
from datetime import datetime
from decimal import Decimal


class PredictResponse(tp.TypedDict):
    figi: str
    for_date: datetime
    next_price: Decimal
