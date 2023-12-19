from datetime import date, timedelta
from operator import and_
from typing import Optional

from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from grocerywebcrawler.models.safeway_item import SafewayItemDBModel
from webserver.models.store import StoreDbModel


class StorePriceObject(BaseModel):
    storeId: Optional[str]
    storeLocation: Optional[str]
    price: Optional[float]
    date: Optional[date]


class PriceComparisonBetweenStores(BaseModel):
    name: Optional[str]
    upc: Optional[str]
    currentDate: Optional[date]
    prices: Optional[list[StorePriceObject]]


def create_price_comparison_between_stores(upc: str, db: Session):
    one_week_ago = date.today() - timedelta(days=7)
    safeway_items: list[SafewayItemDBModel] = db.query(SafewayItemDBModel).filter(
        and_(SafewayItemDBModel.date > one_week_ago, SafewayItemDBModel.upc == upc)).order_by(
        SafewayItemDBModel.date.desc()).all()
    safeway_item_set = set()
    store_id_set = set()
    for item in safeway_items:
        if item.storeId in store_id_set:
            continue
        else:
            safeway_item_set.add(item)
            store_id_set.add(item.storeId)
    stores: list[StoreDbModel] = db.query(StoreDbModel).all()
    store_map = {}
    for store in stores:
        store_map[store.storeId] = store.location

    priceObjects = []
    safeway_item_name = ""
    for safeway_item in safeway_item_set:
        safeway_item_name = safeway_item.name
        store_price_object = StorePriceObject()
        store_price_object.storeId = safeway_item.storeId
        store_price_object.storeLocation = store_map[safeway_item.storeId]
        store_price_object.price = safeway_item.price
        store_price_object.date = safeway_item.date
        priceObjects.append(store_price_object)

    new_price_comparison_object = PriceComparisonBetweenStores()
    new_price_comparison_object.name = safeway_item_name
    new_price_comparison_object.upc = upc
    new_price_comparison_object.currentDate = one_week_ago
    new_price_comparison_object.prices = priceObjects
    return new_price_comparison_object

