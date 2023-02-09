from sqlalchemy import String, Column, TIMESTAMP, Integer


from grocerywebcrawler.models.safeway_item import Base



class OperationDbModel(Base):
    __tablename__ = "operations_table"
    id = Column(String, primary_key=True)
    operationName = Column(String, index=True)
    date = Column(TIMESTAMP)
    totalItems = Column(Integer)
    currentProcessed = Column(Integer)
    storeId = Column(String, index=True)
    status = Column(String, index=True)
    count = Column(Integer)

    def toString(self):
        return f"Operations Record: id:{self.id} totalItems: {self.totalItems} currentProcessed: {self.currentProcessed} status: {self.status}"
