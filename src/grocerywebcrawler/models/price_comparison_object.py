from typing import Optional

from pydantic import BaseModel


class PriceAttributes(BaseModel):
    name: Optional[str]
    upc: Optional[str]
    price: Optional[float]
    basePrice: Optional[float]
    pricePer: Optional[float]
    unitQuantity: Optional[str]
    averageWeight: Optional[str]


class PriceComparisonObject(BaseModel):
    name: Optional[str]
    upc: Optional[str]
    percentageChangeBasePrice: Optional[float]
    basePriceChange: Optional[float]
    priceChange: Optional[float]
    percentageChangePrice: Optional[float]
    pricePerChange: Optional[float]
    percentageChangePricePer: Optional[float]
    price2: Optional[float]
    price1: Optional[float]
