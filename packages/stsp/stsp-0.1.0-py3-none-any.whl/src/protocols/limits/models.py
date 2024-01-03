import typing as tp
from decimal import Decimal as Dec


class MddLimitsResponse(tp.TypedDict):
    """Maximum Drawdown. (%)"""

    day: float | None
    week: float | None
    month: float | None
    year: float | None


CapitalLimitsResponse: tp.TypeAlias = Dec  # Capital Limits


FeeResponse: tp.TypeAlias = float  # fee (%)


TaxRateResponse: tp.TypeAlias = float  # Tax Rate (%)
