from datetime import datetime, timedelta

from grocerywebcrawler.rds_connection import RDSConnection
from webserver.models.price_change_object import PriceChangeDBModel


def clear_price_change_objects():
    db = RDSConnection.get_postgres_session()
    sevenDaysAgo = datetime.now() - timedelta(days=7)
    db.query(PriceChangeDBModel).filter(PriceChangeDBModel.currentDate < sevenDaysAgo).delete()
    db.commit()


if __name__ == '__main__':
    clear_price_change_objects()
