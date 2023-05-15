from grocerywebcrawler.models.safeway_item import Base
from sqlalchemy import Column, String, TIMESTAMP, JSON


class DistinctSafewayItems(Base):
    __tablename__ = "distinct_safeway_items"
    id = Column(String, index=True, primary_key=True)
    upc = Column(String, index=True)
    storeId = Column(String, index=True)
    name = Column(String)
    departmentName = Column(String)
    date = Column(TIMESTAMP)
    area = Column(String)
    storesAvailable = Column(JSON)

# DistinctSafewayItems.__table__.create(RDSConnection.get_engine())
