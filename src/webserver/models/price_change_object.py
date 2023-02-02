from datetime import date
from typing import Optional
from sqlalchemy import Column, String, TIMESTAMP, FLOAT
from sqlalchemy.orm import declarative_base


class PriceChangeObject:
    name: Optional[str]
    upc: Optional[str]
    category: Optional[str]
    priceChange30Days: Optional[float] = 0.0
    price30DaysAgo: Optional[float]
    percentPriceChange30Days: Optional[float] = 0.0
    date30DaysAgo: Optional[date]
    currentPrice: Optional[str]
    currentDate: Optional[date]
    priceChange7Days: Optional[float] = 0.0
    percentPriceChange7Days: Optional[float] = 0.0
    date7DaysAgo: Optional[date]
    price7DaysAgo: Optional[float]
    earliestPrice: Optional[float]
    earliestDate: Optional[date]
    storeId: Optional[str]
    date: Optional[date]

    def to_db_object(self):
        return PriceChangeDBModel(
            id=f"{self.storeId}_{self.upc}_{self.currentDate.strftime('%Y-%m-%d')}", storeId=self.storeId, name=self.name, upc=self.upc,
            category=self.category,
            priceChange30Days=self.priceChange30Days, price30DaysAgo=self.price30DaysAgo,
            percentPriceChange30Days=self.percentPriceChange30Days,
            date30DaysAgo=self.date30DaysAgo, currentPrice=self.currentPrice,
            price7DaysAgo=self.price7DaysAgo,
            priceChange7DaysAgo=self.priceChange7Days,
            percentPriceChange7DaysAgo=self.percentPriceChange7Days,
            date7DaysAgo=self.date7DaysAgo, currentDate=self.currentDate,
            earliestPrice=self.earliestPrice, earliestDate=self.earliestDate,
            absPercentPriceChange7Days=abs(self.percentPriceChange7Days),
            absPercentPriceChange30Days=abs(self.percentPriceChange30Days))


Base = declarative_base()


class PriceChangeDBModel(Base):
    __tablename__ = "price_change_object"
    id = Column(String, primary_key=True, unique=True)
    storeId = Column(String, index=True)
    name = Column(String, index=True)
    upc = Column(String, index=True)
    category = Column(String, index=True)
    priceChange30Days = Column(FLOAT)
    price30DaysAgo = Column(FLOAT)
    percentPriceChange30Days = Column(FLOAT)
    date30DaysAgo = Column(TIMESTAMP)
    currentPrice = Column(FLOAT)
    priceChange7DaysAgo = Column(FLOAT)
    percentPriceChange7DaysAgo = Column(FLOAT)
    date7DaysAgo = Column(TIMESTAMP)
    price7DaysAgo = Column(FLOAT)
    currentDate = Column(TIMESTAMP, index=True)
    earliestPrice = Column(FLOAT)
    earliestDate = Column(TIMESTAMP)
    absPercentPriceChange7Days = Column(FLOAT)
    absPercentPriceChange30Days = Column(FLOAT)

# PriceChangeDBModel.__table__.create(get_engine())
