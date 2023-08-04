from datetime import datetime, timedelta

from grocerywebcrawler.rds_connection import RDSConnection
from webserver.models.price_change_object import PriceChangeDBModel


def clear_price_change_objects():
    db = RDSConnection.get_postgres_session()
    fourteenDaysAgo = datetime.now() - timedelta(days=14)
    db.query(PriceChangeDBModel).filter(PriceChangeDBModel.currentDate < fourteenDaysAgo).all()
    db.commit()


if __name__ == '__main__':
    clear_price_change_objects()
