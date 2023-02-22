from datetime import datetime
from sqlalchemy import Column, Integer, TIMESTAMP
from grocerywebcrawler.models.safeway_item import Base
from grocerywebcrawler.rds_connection import RDSConnection

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, index=True, primary_key=True)
    count = Column(Integer)
    date = Column(TIMESTAMP)


def increment_counter():
    db = RDSConnection.get_postgres_session()
    previous: Counter = db.query(Counter).filter(Counter.id == 1).one()
    db.query(Counter).filter(Counter.id == 1).update({
        Counter.count: previous.count + 1, Counter.date: datetime.now()})
    db.commit()

if __name__ == '__main__':
    increment_counter()
