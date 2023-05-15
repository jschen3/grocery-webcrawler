import datetime
from typing import Optional

from pydantic import BaseModel


class PriceChangeRow(BaseModel):
    startDate: Optional[datetime.date]
    endDate: Optional[datetime.date]
    startDateEndDateStr: Optional[str]
    basePrice: Optional[float]
    currentPrice: Optional[float]
    pricePer: Optional[float]
    unitOfMeasure: Optional[str]
    currentPriceChangeFromToday: Optional[float]
    currentPriceChangePercentageFromToday: Optional[float]
