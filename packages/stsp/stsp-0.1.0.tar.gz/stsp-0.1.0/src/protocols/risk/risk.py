import typing as tp


class RiskProtocol(tp.Protocol):
    def is_account_risk_realized(self) -> bool:
        """Checker provide True if risk for account has been relized"""

    def is_session_risk_realized(self) -> bool:
        """Checker provide True if risk for session (traiding day) has been relized"""

    def is_securities_risk_realized(self) -> bool:
        """Checker provide True if risk for securities has been relized"""
