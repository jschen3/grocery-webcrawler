from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP

from grocerywebcrawler.models.safeway_item import Base
from grocerywebcrawler.rds_connection import RDSConnection
from webserver.models.operation_db_model import OperationDbModel


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


def lowercase_status():
    db = RDSConnection.get_postgres_session()
    operations: OperationDbModel = db.query(OperationDbModel).all()
    for operation in operations:
        db.query(OperationDbModel).filter(OperationDbModel.id == operation.id).update({
            OperationDbModel.status: operation.status.lower()
        })
    db.commit()


if __name__ == '__main__':
    increment_counter()
    # lowercase_status()
