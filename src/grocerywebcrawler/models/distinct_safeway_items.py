from grocerywebcrawler.models.safeway_item import Base
from sqlalchemy import Column, String, TIMESTAMP


class DistinctSafewayItem(Base):
    __tablename__ = "distinct_safeway_item"
    upc = Column(String, index=True, primary_key=True)
    storeId = Column(String, index=True)
    name = Column(String)
    departmentName = Column(String)
    date = Column(TIMESTAMP)
    area = Column(String)

