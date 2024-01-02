from datetime import date
from typing import Optional

from pydantic.main import BaseModel


class ShoppingListItem(BaseModel):
    index:Optional[int]
    updatedDate: Optional[date]
    itemName: Optional[str]
    upc: Optional[str]
    cheapestPrice: Optional[float] = 0.0
    cheapestPriceLocation: Optional[str]
    highestPrice: Optional[float] = 0.0
    highestPriceLocation: Optional[str]
