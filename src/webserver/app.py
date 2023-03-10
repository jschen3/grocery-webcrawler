import io
import json
import pytz  # $ pip install pytz
import tzlocal  # $ pip install tzlocal
import pandas
from datetime import datetime, timedelta, date

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, asc
from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from grocerywebcrawler.models.safeway_item import SafewayItemDBModel, SafewayItem
from fastapi.middleware.cors import CORSMiddleware
from grocerywebcrawler.rds_connection import RDSConnection
from webserver.build_general_info_section import build_general_information
from counter import Counter
from webserver.models.operation_db_model import OperationDbModel
from webserver.models.price_change_row import PriceChangeRow
from webserver.models.store import StoreDbModel, Store

from webserver.models.price_change_object import PriceChangeDBModel

from util.logging import info

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
    db = RDSConnection.get_normal_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/regions")
async def get_regions():
    info("testing logging quickly inside docker")
    return {"regions": ["bay-area"]}  # later when more regions are available update


@app.get("/stores/{region}")
async def getStoreFromRegion(region: str, db: Session = Depends(get_db)) -> list[Store]:
    store_query_results: list[StoreDbModel] = db.query(StoreDbModel).where(StoreDbModel.region == region)
    stores = []
    for store in store_query_results:
        stores.append(store.to_store_object())
    return stores


@app.get("/items/{storeId}")
async def getItemsFromStore(storeId: str, q: str, limit: int = 30, db: Session = Depends(get_db)):
    split_q = q.split(" ")
    like_phrase = f"%{'%'.join(split_q)}%"
    safeway_items_from_query: list[DistinctSafewayItem] = db.query(DistinctSafewayItem.name, DistinctSafewayItem.upc,
                                                                   DistinctSafewayItem.storeId).filter(and_(
        DistinctSafewayItem.storeId == storeId,
        func.lower(DistinctSafewayItem.name).like(func.lower(like_phrase)))).order_by(DistinctSafewayItem.name).limit(
        limit).all()
    return safeway_items_from_query


@app.get("/items/{storeId}/{upc}/prices")
async def getPricesOfItem(storeId: str, upc: str, days: int, db: Session = Depends(get_db)):
    days_before = (datetime.today() - timedelta(days=days)).date()
    query = db.query(SafewayItemDBModel.name, SafewayItemDBModel.upc, SafewayItemDBModel.date, SafewayItemDBModel.price,
                     SafewayItemDBModel.basePrice, SafewayItemDBModel.pricePer).filter(and_(
        SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc,
        SafewayItemDBModel.date > days_before)).order_by(
        asc(SafewayItemDBModel.date))

    df = pandas.read_sql_query(query.statement, con=RDSConnection.get_engine())
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="application/csv")
    return response


@app.get("/items/{storeId}/{upc}/json/prices")
async def getPricesOfItemJson(storeId: str, upc: str, days: int = -1, db: Session = Depends(get_db)):
    return getPricesOfItemJsonHelper(storeId, upc, days, db)


def getPricesOfItemJsonHelper(storeId: str, upc: str, days: int, db: Session):
    if days == -1:
        return getDataFrameJsonObject(storeId, upc, None, db)
    else:
        days_before = (datetime.today() - timedelta(days=days)).date()
        return getDataFrameJsonObject(storeId, upc, days_before, db)


def getDataFrameJsonObject(storeId, upc, days_before, db):
    if days_before is None:
        query = db.query(SafewayItemDBModel).filter(and_(
            SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc))
    else:
        query = db.query(SafewayItemDBModel).filter(and_(
            SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc,
            SafewayItemDBModel.date > days_before))
    df = pandas.read_sql_query(query.statement, con=RDSConnection.get_engine())

    jsonResponse = json.loads(df.to_json(orient='records'))
    newJsonResponse = []
    for entry in jsonResponse:
        currentDate = datetime.fromtimestamp(int(entry['date'] / 1000))
        entry['date'] = currentDate.strftime("%Y-%m-%d")
        newJsonResponse.append(entry)
    sortedJson = sorted(newJsonResponse, key=lambda x: x['date'], reverse=False)
    return sortedJson


@app.get("/items/{storeId}/{upc}")
async def getItem(storeId: str, upc: str, db: Session = Depends(get_db)):
    general_info = build_general_information(storeId=storeId, upc=upc, db=db)
    return general_info


@app.get("/greatest_price_changes")
async def greatest_price_changes(storeId: str = "2948", limit: int = 30, offset: int = 0, thirtyOr7Days: bool = False,
                                 db: Session = Depends(get_db)):
    # don't know why this query doesn't quite work. The distinct piece doesn't work....

    if thirtyOr7Days:
        thirty_days_ago = date.today() - timedelta(
            days=30)  # a price change occurred in the last 7 days. Compared to the price 7 days ago was one of the top 50 greatest price changes.
        greatest_percent_items: list[PriceChangeDBModel] = db.query(PriceChangeDBModel.upc,
                                                                    PriceChangeDBModel.name,
                                                                    PriceChangeDBModel.storeId,
                                                                    PriceChangeDBModel.category,
                                                                    PriceChangeDBModel.price7DaysAgo,
                                                                    PriceChangeDBModel.price30DaysAgo,
                                                                    PriceChangeDBModel.currentPrice,
                                                                    PriceChangeDBModel.priceChange7DaysAgo,
                                                                    PriceChangeDBModel.priceChange30Days,
                                                                    PriceChangeDBModel.percentPriceChange7DaysAgo,
                                                                    PriceChangeDBModel.percentPriceChange30Days,
                                                                    PriceChangeDBModel.absPercentPriceChange7Days,
                                                                    PriceChangeDBModel.absPercentPriceChange30Days,
                                                                    PriceChangeDBModel.currentDate).filter(and_(
            PriceChangeDBModel.currentDate > thirty_days_ago, PriceChangeDBModel.storeId == storeId)).order_by(
            PriceChangeDBModel.absPercentPriceChange30Days.desc()).limit(
            limit * 10).offset(offset).all()
    else:
        one_week_ago = date.today() - timedelta(days=7)
        greatest_percent_items: list[PriceChangeDBModel] = db.query(PriceChangeDBModel.upc,
                                                                    PriceChangeDBModel.name,
                                                                    PriceChangeDBModel.storeId,
                                                                    PriceChangeDBModel.category,
                                                                    PriceChangeDBModel.price7DaysAgo,
                                                                    PriceChangeDBModel.price30DaysAgo,
                                                                    PriceChangeDBModel.currentPrice,
                                                                    PriceChangeDBModel.priceChange7DaysAgo,
                                                                    PriceChangeDBModel.priceChange30Days,
                                                                    PriceChangeDBModel.percentPriceChange7DaysAgo,
                                                                    PriceChangeDBModel.percentPriceChange30Days,
                                                                    PriceChangeDBModel.absPercentPriceChange7Days,
                                                                    PriceChangeDBModel.absPercentPriceChange30Days,
                                                                    PriceChangeDBModel.currentDate).filter(and_(
            PriceChangeDBModel.currentDate > one_week_ago, PriceChangeDBModel.storeId == storeId)).order_by(
            PriceChangeDBModel.absPercentPriceChange7Days.desc()).limit(
            limit * 10).offset(offset).all()

    upcs = set()
    items = []
    for item in greatest_percent_items:
        if item.upc in upcs:
            continue
        else:
            upcs.add(item.upc)
            items.append(item)
    if limit < len(items):
        return items[0:limit]
    else:
        return items


@app.get("/operations")
def getOperations(operation: str = "webcrawl", status: str = "finished", db: Session = Depends(get_db)):
    return db.query(OperationDbModel).filter(
        and_(OperationDbModel.operationName == operation.lower(), OperationDbModel.status == status)).order_by(
        OperationDbModel.intId.desc()).all()


@app.get("/counter")
def getCounter(db: Session = Depends(get_db)):
    count: list[Counter] = db.query(Counter).all()
    utc_date = count[0].date
    local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
    local_time = utc_date.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    count[0].date = local_time
    return count


@app.get("/pricechangetable/{storeId}/{upc}")
def priceChangeTable(upc: str, storeId: str, days: int = -1, db: Session = Depends(get_db)):
    price_change_dataframe: list[dict] = getPricesOfItemJsonHelper(storeId=storeId, upc=upc, days=days, db=db)
    if price_change_dataframe != None and len(price_change_dataframe) > 0:
        """
        Price Range
        [start, end]   | Price   | Percentage from today...
        """
        latestRow = SafewayItem.parse_obj(price_change_dataframe[len(price_change_dataframe) - 1])
        latestPrice = latestRow.price
        priceChangeRows = []
        currentPriceChangeRow = None
        for dataframe_item in enumerate(price_change_dataframe):
            item = SafewayItem.parse_obj(dataframe_item[1])
            if dataframe_item[0] == 0:
                currentPriceChangeRow = PriceChangeRow()
                currentPriceChangeRow.startDate = item.date
                currentPriceChangeRow.currentPrice = item.price
                currentPriceChangeRow.basePrice = item.basePrice
                currentPriceChangeRow.pricePer = item.pricePer
                currentPriceChangeRow.unitOfMeasure = item.unitOfMeasure
            if item.price != currentPriceChangeRow.currentPrice:
                currentPriceChangeRow.endDate = item.date
                currentPriceChangeRow.currentPriceChangeFromToday = currentPriceChangeRow.currentPrice - latestPrice
                currentPriceChangeRow.currentPriceChangePercentageFromToday = (currentPriceChangeRow.currentPriceChangeFromToday / currentPriceChangeRow.currentPrice)*100
                currentPriceChangeRow.startDateEndDateStr = f"{currentPriceChangeRow.startDate.strftime('%B %d, %Y')} -- {currentPriceChangeRow.endDate.strftime('%B %d, %Y')}"
                priceChangeRows.append(currentPriceChangeRow.copy())
                currentPriceChangeRow = PriceChangeRow()
                currentPriceChangeRow.startDate = item.date
                currentPriceChangeRow.currentPrice = item.price
                currentPriceChangeRow.basePrice = item.basePrice
                currentPriceChangeRow.pricePer = item.pricePer
                currentPriceChangeRow.unitOfMeasure = item.unitOfMeasure

        if priceChangeRows[len(priceChangeRows) - 1].currentPrice != latestPrice:
            currentPriceChangeRow.endDate = latestRow.date
            currentPriceChangeRow.currentPriceChangeFromToday = currentPriceChangeRow.currentPrice - latestPrice
            currentPriceChangeRow.currentPriceChangePercentageFromToday = (currentPriceChangeRow.currentPriceChangeFromToday / currentPriceChangeRow.currentPrice) * 100
            currentPriceChangeRow.startDateEndDateStr = f"{currentPriceChangeRow.startDate.strftime('%B %d, %Y')} -- {currentPriceChangeRow.endDate.strftime('%B %d, %Y')}"
            priceChangeRows.append(currentPriceChangeRow.copy())
        return priceChangeRows
