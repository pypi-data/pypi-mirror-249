import typing as tp
from decimal import Decimal as Dec


class EntryPointResponse(tp.TypedDict):
    price: Dec
    volume: int | None


class ExitPointResponse(tp.TypedDict):
    price: Dec
    volume: int | None
