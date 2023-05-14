import json
from datetime import date
from operator import and_
from typing import Optional

from pydantic.main import BaseModel

from grocerywebcrawler.models.safeway_item import SafewayItem, SafewayItemDBModel
from grocerywebcrawler.rds_connection import RDSConnection
from webserver.models.store import StoreDbModel
from sqlalchemy.orm import Session


class StorePriceObject(BaseModel):
    storeId: Optional[str]
    storeLocation: Optional[str]
    price: Optional[float]


class PriceComparisonBetweenStores(BaseModel):
    name: Optional[str]
    upc: Optional[str]
    currentDate: Optional[date]
    prices: Optional[list[StorePriceObject]]


def create_price_comparison_between_stores(upc: str, db: Session):
    today = date.today()
    safeway_items: list[SafewayItemDBModel] = db.query(SafewayItemDBModel).filter(
        and_(SafewayItemDBModel.date == today, SafewayItemDBModel.upc == upc)).all()

    stores: list[StoreDbModel] = db.query(StoreDbModel).all()
    store_map = {}
    for store in stores:
        store_map[store.storeId] = store.location

    priceObjects = []
    safeway_item_name = ""
    for safeway_item in safeway_items:
        safeway_item_name = safeway_item.name
        store_price_object = StorePriceObject()
        store_price_object.storeId = safeway_item.storeId
        store_price_object.storeLocation = store_map[safeway_item.storeId]
        store_price_object.price = safeway_item.price
        priceObjects.append(store_price_object)

    new_price_comparison_object = PriceComparisonBetweenStores()
    new_price_comparison_object.name = safeway_item_name
    new_price_comparison_object.upc = upc
    new_price_comparison_object.currentDate = today
    new_price_comparison_object.prices = priceObjects
    return new_price_comparison_object

#print(create_price_comparison_between_stores('0004200015810', None))
