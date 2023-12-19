import io
import json
from datetime import datetime, timedelta

import pandas
import pytz
import tzlocal
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi_utils.tasks import repeat_every
from sqlalchemy import func, and_, asc
from sqlalchemy.orm import Session

from counter import Counter
from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItems
from grocerywebcrawler.models.safeway_item import SafewayItemDBModel, SafewayItem
from grocerywebcrawler.rds_connection import RDSConnection
from util.logging import info
from webserver.build_general_info_section import build_general_information
from webserver.greatest_price_changes_cache import GreatestPriceChangesCache
from webserver.models.operation_db_model import OperationDbModel
from webserver.models.price_change_row import PriceChangeRow
from webserver.models.store import StoreDbModel, Store
from webserver.price_comparison_between_stores import create_price_comparison_between_stores

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


@app.on_event('startup')
@repeat_every(seconds=60 * 60)  # 1 hour
def scheduled_tasks():
    RDSConnection.clear_normal_session()
    GreatestPriceChangesCache.clear_cache()


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


@app.get("/storeinfo/{storeId}")
async def getStoreInfo(storeId: str, db: Session = Depends(get_db)) -> Store:
    stores: list[StoreDbModel] = db.query(StoreDbModel).filter(StoreDbModel.storeId == storeId).all()
    storeList = []
    for store in stores:
        storeList.append(store.to_store_object())
    if len(storeList) > 0:
        return storeList[0]
    else:
        return None


@app.get("/items/{storeId}")
async def getItemsFromStore(storeId: str, q: str, limit: int = 30, db: Session = Depends(get_db)):
    split_q = q.split(" ")
    like_phrase = f"%{'%'.join(split_q)}%"
    safeway_items_from_query: list[DistinctSafewayItems] = db.query(DistinctSafewayItems.name, DistinctSafewayItems.upc,
                                                                    DistinctSafewayItems.storeId).filter(and_(
        DistinctSafewayItems.storeId == storeId,
        func.lower(DistinctSafewayItems.name).like(func.lower(like_phrase)))).order_by(DistinctSafewayItems.name).limit(
        limit).all()
    return safeway_items_from_query


@app.get("/items/{storeId}/{upc}/prices")
async def getPricesOfItem(storeId: str, upc: str, days: int, db: Session = Depends(get_db)):
    today = datetime.today()
    date_string = '2023-08-09'
    august_date = datetime.strptime(date_string, "%Y-%m-%d")
    days_before = (today - timedelta(days=days)).date()
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
        today = datetime.today()
        date_string = '2023-08-09'
        august_date = datetime.strptime(date_string, "%Y-%m-%d")
        days_before = (today - timedelta(days=days)).date()
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
    greatest_percent_items = GreatestPriceChangesCache.get_greatest_price_changes(storeId=storeId, limit=limit,
                                                                                  offset=offset,
                                                                                  thirtyOr7Days=thirtyOr7Days, db=db)
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
def getOperations(operation: str = "webcrawl", status: str = "finished", store: str = None, limit: int = 50,
                  db: Session = Depends(get_db)):
    if store is None:
        return db.query(OperationDbModel).filter(
            and_(OperationDbModel.operationName == operation.lower(), OperationDbModel.status == status)).order_by(
            OperationDbModel.intId.desc()).limit(limit).all()
    else:
        return db.query(OperationDbModel).filter(and_(
            and_(OperationDbModel.operationName == operation.lower(), OperationDbModel.status == status),
            OperationDbModel.storeId == store)).order_by(
            OperationDbModel.intId.desc()).limit(limit).all()


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
                currentPriceChangeRow.currentPriceChangePercentageFromToday = (
                                                                                      currentPriceChangeRow.currentPriceChangeFromToday / currentPriceChangeRow.currentPrice) * 100
                currentPriceChangeRow.startDateEndDateStr = f"{currentPriceChangeRow.startDate.strftime('%B %d, %Y')} -- {currentPriceChangeRow.endDate.strftime('%B %d, %Y')}"
                priceChangeRows.append(currentPriceChangeRow.copy())
                currentPriceChangeRow = PriceChangeRow()
                currentPriceChangeRow.startDate = item.date
                currentPriceChangeRow.currentPrice = item.price
                currentPriceChangeRow.basePrice = item.basePrice
                currentPriceChangeRow.pricePer = item.pricePer
                currentPriceChangeRow.unitOfMeasure = item.unitOfMeasure

        if len(priceChangeRows) == 0 or priceChangeRows[len(priceChangeRows) - 1].currentPrice != latestPrice:
            currentPriceChangeRow.endDate = latestRow.date
            currentPriceChangeRow.currentPriceChangeFromToday = currentPriceChangeRow.currentPrice - latestPrice
            currentPriceChangeRow.currentPriceChangePercentageFromToday = (
                                                                                  currentPriceChangeRow.currentPriceChangeFromToday / currentPriceChangeRow.currentPrice) * 100
            currentPriceChangeRow.startDateEndDateStr = f"{currentPriceChangeRow.startDate.strftime('%B %d, %Y')} -- {currentPriceChangeRow.endDate.strftime('%B %d, %Y')}"
            priceChangeRows.append(currentPriceChangeRow.copy())
        return priceChangeRows


@app.get("/pricecomparison/{upc}")
def priceComparison(upc: str, db: Session = Depends(get_db)):
    return create_price_comparison_between_stores(upc, db)
