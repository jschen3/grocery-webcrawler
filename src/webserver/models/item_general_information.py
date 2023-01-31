from typing import Optional
from datetime import date


class ItemGeneralInformation:
    name: Optional[str]
    upc: Optional[str]
    date: Optional[date]
    price: Optional[str]
    basePrice: Optional[str]
    pricePer: Optional[str]
    storeId: Optional[str]
    storeLocation: Optional[str]
    price7DaysAgo: Optional[float]
    priceChangeLast7Days: Optional[float]
    percentPriceChange7Days: Optional[float]
    price30DaysAgo: Optional[float]
    priceChangeLast30days: Optional[float]
    percentPriceChange30days: Optional[float]
    earliestPrice: Optional[float]
    percentPriceChangeForAllRecords: Optional[float]
    priceChangeForAllRecords: Optional[float]
    category: Optional[str]
    itemsInCategory: Optional[list[tuple]]
    priceOfAllItemsInCategory: Optional[float]
    priceOfAllItemsInCategory7Days: Optional[float]
    priceOfAllItemsInCategory30Days: Optional[float]
    lowestPriceAtLocalStores: Optional[str]
    highestPriceAtLocalStores: Optional[str]
    earliestDatePriceAvailable: Optional[str]

    def dict(self):
        return {
            "name": self.name,
            "upc": self.upc,
            "price": self.price,
            "basePrice": self.basePrice,
            "pricePer": self.pricePer,
            "storeId": self.storeId,
            "storeLocation": self.storeLocation,
            "priceChangeLast7Days": self.priceChangeLast7Days,
            "percentPriceChange7Days": self.priceChangeLast7Days,
            "priceChangeLast30Days": self.priceChangeLast30days,
            "percentPriceChangeLast30Days": self.percentPriceChange30days,
            "percentPriceChangeForAllRecords": self.percentPriceChangeForAllRecords,
            "priceChangeForAllRecords": self.priceChangeForAllRecords,
            "category": self.category,
            "itemsInCategory": self.itemsInCategory,
            "priceOfAllItemsInCategory": self.priceOfAllItemsInCategory,
            "pricePerCategory": self.pricePerCategory,
            "similarItemsFromName": self.similarItemsFromName,
            "priceOfAllSimilarName": self.priceOfAllSimilarName,
            "lowestPriceAtLocalStores": self.lowestPriceAtLocalStores,
            "highestPriceAtLocalStores": self.highestPriceAtLocalStores,
            "earliestDatePriceAvailable": self.earliestDatePriceAvailable
        }
# think about name

# create a database of unique name and upc.
# and store
