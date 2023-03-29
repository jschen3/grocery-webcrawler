import time

from grocerywebcrawler.rds_connection import RDSConnection
from grocerywebcrawler.safeway_crawler import get_all_safeway_items_from_store
from webserver.models.store import StoreDbModel


def webcrawl():
    db = RDSConnection.get_postgres_session()
    stores: list[StoreDbModel] = db.query(StoreDbModel).all()
    for store in stores:
        if store.webcrawl:
            get_all_safeway_items_from_store(store.storeId)
            time.sleep(60)


if __name__ == '__main__':
    webcrawl()
