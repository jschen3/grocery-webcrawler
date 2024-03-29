from grocerywebcrawler.models.safeway_item import Base
from sqlalchemy import String, Column, TIMESTAMP, Integer


class OperationDbModel(Base):
    __tablename__ = "operations_table"
    id = Column(String, primary_key=True)
    intId = Column(Integer)
    countToday = Column(Integer)
    operationName = Column(String, index=True)
    date = Column(TIMESTAMP)
    totalItems = Column(Integer)
    newItems = Column(Integer)
    prevItemCount = Column(Integer)
    storeId = Column(String, index=True)
    status = Column(String, index=True)
    itemsCrawled = Column(Integer)

    def toString(self):
        return f"Operations Record: id:{self.id} totalItems: {self.totalItems} newItems: {self.newItems} prevItemCount: {self.prevItemCount} status: {self.status} intId: {self.intId} countToday: {self.countToday}"
