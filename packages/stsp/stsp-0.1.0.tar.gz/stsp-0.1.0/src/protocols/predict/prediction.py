"""Protocol for predict"""

import typing as tp

from src.protocols.models.common import OHLC
from src.protocols.predict.models import PredictResponse


class PredictionProtocol(tp.Protocol):
    async def predict(
        self,
        *,
        figi: str,
        current_ohlc: OHLC,
    ) -> list[PredictResponse]:
        """Predcit next N prices"""
