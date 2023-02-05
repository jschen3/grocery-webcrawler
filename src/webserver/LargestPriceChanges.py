import multiprocessing
import traceback
from datetime import datetime, timedelta

from grocerywebcrawler.models.safeway_item import SafewayItem
from sqlalchemy.exc import NoResultFound

from grocerywebcrawler.rds_connection import get_postgres_session

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from webserver.build_general_info_section import allTimeDataframe, calculatePriceChangeDays
from webserver.models.price_change_object import PriceChangeObject, PriceChangeDBModel


def setStandardFields(item:DistinctSafewayItem, safeway_items:list[SafewayItem], priceChangeObject: PriceChangeObject):
    earliestDate = datetime.strptime(safeway_items[0]["date"], '%Y-%m-%d')
    priceChangeObject.upc = item.upc
    priceChangeObject.storeId = item.storeId
    priceChangeObject.name = item.name
    priceChangeObject.earliestDate = earliestDate
    priceChangeObject.earliestPrice = safeway_items[0]["price"]
    priceChangeObject.currentPrice = safeway_items[len(safeway_items) - 1]["price"]
    priceChangeObject.category = item.departmentName


def process_and_find_price_changes(i):
    print(f"processing and find changes for items start at i: {i}")
    db = get_postgres_session()
    priceChangeObjects: list[PriceChangeObject] = []
    all_distinct_items: list[DistinctSafewayItem] = db.query(DistinctSafewayItem).offset(i).limit(
        50).all()  # put a limit and do it in fragments
    print(f"start: {i} limit: 50")
    for index, item in enumerate(all_distinct_items):
        currentDate = datetime.today()
        all_time_dataframe = allTimeDataframe(item.storeId, item.upc, db)

        priceChangeObject: PriceChangeObject = PriceChangeObject()
        sevenDaysAgo = currentDate - timedelta(days=7)
        sevenDayPriceChangeObject = calculatePriceChangeDays(all_time_dataframe, sevenDaysAgo, currentDate)
        priceChangeObject.price7DaysAgo = sevenDayPriceChangeObject["firstPrice"]
        priceChangeObject.date7DaysAgo = sevenDayPriceChangeObject["startDate"]
        priceChangeObject.currentPrice = sevenDayPriceChangeObject["lastPrice"]
        priceChangeObject.currentDate = currentDate
        priceChangeObject.percentPriceChange7Days = sevenDayPriceChangeObject["percentPriceChange"]
        priceChangeObject.priceChange7Days = sevenDayPriceChangeObject["priceChange"]

        thirtyDaysAgo = currentDate - timedelta(days=30)
        thirtyDayPriceChangeObject = calculatePriceChangeDays(all_time_dataframe, thirtyDaysAgo, currentDate)
        priceChangeObject.price30DaysAgo = thirtyDayPriceChangeObject["firstPrice"]
        priceChangeObject.date30DaysAgo = thirtyDayPriceChangeObject["startDate"]
        priceChangeObject.percentPriceChange30Days = thirtyDayPriceChangeObject["percentPriceChange"]
        priceChangeObject.priceChange30Days = thirtyDayPriceChangeObject["priceChange"]

        priceChangeObject.earliestPrice = SafewayItem.parse_obj(all_time_dataframe[0]).price
        priceChangeObject.earliestDate = SafewayItem.parse_obj(all_time_dataframe[0]).date
        priceChangeObject.priceChangeForAllRecords = priceChangeObject.earliestPrice - priceChangeObject.currentPrice
        priceChangeObject.percentPriceChangeForAllRecords = float('{:0.2f}'.format((
                                                                    priceChangeObject.priceChangeForAllRecords / priceChangeObject.earliestPrice) * 100))
        setStandardFields(item, all_time_dataframe, priceChangeObject)
        if abs(priceChangeObject.priceChange30Days) > 0 or abs(priceChangeObject.priceChange7Days) > 0:
            db_object = priceChangeObject.to_db_object()
            try:
                existing = db.query(PriceChangeDBModel).filter(PriceChangeDBModel.id == db_object.id).one()
            except NoResultFound:
                db.add(db_object)
                print(
                    f"upc: {db_object.upc} name: {db_object.name} percentPriceChange7days: {db_object.percentPriceChange7DaysAgo} priceChange7Days: {db_object.priceChange7DaysAgo} priceChange30days: {db_object.priceChange30Days} percentPriceChange30Days: {db_object.percentPriceChange30Days}")

    db.commit()
    print(f"Found price changes for items {i} through {i + 50}. Added to price change objects database.")


def createPriceChangeObjects():
    db = get_postgres_session()
    count = db.query(DistinctSafewayItem.upc).count()
    print(f"determining total distinct items. Total items {count}")

    original_number_of_price_change_objects = db.query(PriceChangeDBModel).count()
    print(f"Original Number of Price Change Objects: {original_number_of_price_change_objects}. date: {datetime.now()}")
    ranges = []
    for i in range(0, count, 50):
        ranges.append(i)
    start = datetime.now()
    try:
        pool_obj = multiprocessing.Pool()
        pool_obj.map(process_and_find_price_changes, ranges)
    except Exception:
        print(f"An exception occurred {traceback.format_exc()}")
    print(f'Time taken: {datetime.now() - start}')
    newCount = db.query(PriceChangeDBModel).count()
    print(
        f"New price change objects. {newCount - original_number_of_price_change_objects}. original_count: {original_number_of_price_change_objects} total_items: {newCount} time: {datetime.now()}")
