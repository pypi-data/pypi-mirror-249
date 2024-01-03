import typing as tp

from src.protocols.limits.models import (
    CapitalLimitsResponse,
    FeeResponse,
    MddLimitsResponse,
    TaxRateResponse,
)


class LimitProtocol(tp.Protocol):
    def mdd(self) -> MddLimitsResponse:
        """Maximum Drawdown provider (%)"""

    def capital(self) -> CapitalLimitsResponse:
        """Capital limits response"""

    def fee(self) -> FeeResponse:
        """Fee provider (%)"""

    def tax_rate(self) -> TaxRateResponse:
        """Tax rate provider (%)"""
