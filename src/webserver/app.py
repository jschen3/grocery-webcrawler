import io
import json
import pandas
from datetime import datetime, timedelta, date
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, asc
from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from grocerywebcrawler.models.safeway_item import SafewayItemDBModel
from fastapi.middleware.cors import CORSMiddleware

from grocerywebcrawler.rds_connection import get_normal_session, get_engine
from webserver.build_general_info_section import build_general_information
from webserver.models.store import StoreDbModel, Store

from webserver.models.price_change_object import PriceChangeDBModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def get_db():
    db = get_normal_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/regions")
async def get_regions():
    return {"regions": ["bay-area"]}  # later when more regions are available update


@app.get("/stores/{region}")
async def getStoreFromRegion(region: str, db: Session = Depends(get_db)) -> list[Store]:
    store_query_results: list[StoreDbModel] = db.query(StoreDbModel).where(StoreDbModel.region == region)
    stores = []
    for store in store_query_results:
        stores.append(store.to_store_object())
    return stores


@app.get("/items/{store}")
async def getItemsFromStore(store: str, q: str, limit: int = 30, db: Session = Depends(get_db)):
    split_q = q.split(" ")
    like_phrase = f"%{'%'.join(split_q)}%"
    safeway_items_from_query: list[DistinctSafewayItem] = db.query(DistinctSafewayItem.name, DistinctSafewayItem.upc,
                                                                   DistinctSafewayItem.storeId).filter(and_(
        DistinctSafewayItem.storeId == store,
        func.lower(DistinctSafewayItem.name).like(func.lower(like_phrase)))).order_by(DistinctSafewayItem.name).limit(
        limit).all()
    return safeway_items_from_query


@app.get("/items/{store}/{upc}/prices")
async def getPricesOfItem(store: str, upc: str, days: int, db: Session = Depends(get_db)):
    days_before = (datetime.today() - timedelta(days=days)).date()
    query = db.query(SafewayItemDBModel.name, SafewayItemDBModel.upc, SafewayItemDBModel.date, SafewayItemDBModel.price,
                     SafewayItemDBModel.basePrice, SafewayItemDBModel.pricePer).filter(and_(
        SafewayItemDBModel.storeId == store, SafewayItemDBModel.upc == upc,
        SafewayItemDBModel.date > days_before)).order_by(
        asc(SafewayItemDBModel.date))

    df = pandas.read_sql_query(query.statement, con=get_engine())
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="application/csv")
    return response


@app.get("/items/{store}/{upc}/json/prices")
async def getPricesOfItemJson(store: str, upc: str, days: int, db: Session = Depends(get_db)):
    days_before = (datetime.today() - timedelta(days=days)).date()
    return getDataFrameJsonObject(store, upc, days_before, db)


def getDataFrameJsonObject(storeId, upc, days_before, db):
    query = db.query(SafewayItemDBModel.name, SafewayItemDBModel.upc, SafewayItemDBModel.date, SafewayItemDBModel.price,
                     SafewayItemDBModel.basePrice, SafewayItemDBModel.pricePer).filter(and_(
        SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc,
        SafewayItemDBModel.date > days_before)).order_by(
        asc(SafewayItemDBModel.date))
    df = pandas.read_sql_query(query.statement, con=get_engine())

    jsonResponse = json.loads(df.to_json(orient='records'))
    newJsonResponse = []
    for entry in jsonResponse:
        currentDate = datetime.fromtimestamp(int(entry['date'] / 1000))
        entry['date'] = currentDate.strftime("%Y-%m-%d")
        newJsonResponse.append(entry)
    return newJsonResponse


@app.get("/items/{storeId}/{upc}")
async def getItem(storeId: str, upc: str, db: Session = Depends(get_db)):
    general_info = build_general_information(storeId=storeId, upc=upc, db=db)
    return general_info


@app.get("/greatest_price_changes")
async def greatest_price_changes(limit: int = 30, offset: int = 0, thirtyOr7Days: bool = False,
                                 db: Session = Depends(get_db)):
    yesterday = date.today() - timedelta(days=1)
    if thirtyOr7Days:
        greatest_percent_items = db.query(PriceChangeDBModel.upc.distinct(), PriceChangeDBModel.name,
                                          PriceChangeDBModel.storeId,
                                          PriceChangeDBModel.upc, PriceChangeDBModel.category,
                                          PriceChangeDBModel.price7DaysAgo,
                                          PriceChangeDBModel.price30DaysAgo,
                                          PriceChangeDBModel.currentPrice, PriceChangeDBModel.priceChange7DaysAgo,
                                          PriceChangeDBModel.priceChange30Days,
                                          PriceChangeDBModel.percentPriceChange7DaysAgo,
                                          PriceChangeDBModel.percentPriceChange30Days,
                                          PriceChangeDBModel.absPercentPriceChange7Days,
                                          PriceChangeDBModel.absPercentPriceChange30Days).filter(
            PriceChangeDBModel.currentDate > yesterday).order_by(
            PriceChangeDBModel.absPercentPriceChange30Days.desc()).limit(
            limit).offset(offset).all()
    else:
        greatest_percent_items = db.query(PriceChangeDBModel.upc.distinct(), PriceChangeDBModel.name,
                                          PriceChangeDBModel.upc, PriceChangeDBModel.storeId,
                                          PriceChangeDBModel.category,
                                          PriceChangeDBModel.price7DaysAgo,
                                          PriceChangeDBModel.price30DaysAgo,
                                          PriceChangeDBModel.currentPrice, PriceChangeDBModel.priceChange7DaysAgo,
                                          PriceChangeDBModel.priceChange30Days,
                                          PriceChangeDBModel.percentPriceChange7DaysAgo,
                                          PriceChangeDBModel.percentPriceChange30Days,
                                          PriceChangeDBModel.absPercentPriceChange7Days,
                                          PriceChangeDBModel.absPercentPriceChange30Days).filter(
            PriceChangeDBModel.currentDate > yesterday).order_by(
            PriceChangeDBModel.absPercentPriceChange7Days.desc()).limit(
            limit).offset(offset).all()

    return greatest_percent_items
