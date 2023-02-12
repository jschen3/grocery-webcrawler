import json
from bisect import bisect_left
from datetime import datetime, timedelta
import random

from sqlalchemy import and_, asc
import pandas

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from grocerywebcrawler.models.safeway_item import SafewayItemDBModel, SafewayItem
from grocerywebcrawler.rds_connection import RDSConnection
from webserver.models.item_general_information import ItemGeneralInformation


def fillOut5ItemsInCategory(currentItemGeneralInformation, storeId, db):
    category = currentItemGeneralInformation.category
    all_items_in_category = db.query(DistinctSafewayItem.upc, DistinctSafewayItem.name).where(and_(
        DistinctSafewayItem.departmentName == category, DistinctSafewayItem.storeId == storeId)).all()
    similar_items = []
    if len(all_items_in_category) > 5:
        ten_random_numbers = set()
        while len(ten_random_numbers) < 5:
            random_number = random.randint(0, len(all_items_in_category) - 1)
            ten_random_numbers.add(random_number)
        for random_number in ten_random_numbers:
            similar_items.append(all_items_in_category[random_number])
    else:
        similar_items.extend(all_items_in_category)
    currentItemGeneralInformation.itemsInCategory = []
    for item in similar_items:
        currentItemGeneralInformation.itemsInCategory.append({
            "upc": item.upc, "name": item.name})


def fillOutGeneralInformation(itemGeneralInformation, storeId, upc, db):
    todays_info: SafewayItemDBModel = db.query(SafewayItemDBModel).where(
        and_(SafewayItemDBModel.upc == upc, SafewayItemDBModel.storeId == storeId)).order_by(
        SafewayItemDBModel.date.desc()).all()[0]
    itemGeneralInformation.name = todays_info.name
    itemGeneralInformation.upc = todays_info.upc
    itemGeneralInformation.price = todays_info.price
    itemGeneralInformation.basePrice = todays_info.basePrice
    itemGeneralInformation.pricePer = todays_info.pricePer
    itemGeneralInformation.storeId = todays_info.storeId
    itemGeneralInformation.storeLocation = ""  # get from store table
    itemGeneralInformation.category = todays_info.departmentName
    itemGeneralInformation.date = todays_info.date


def build_general_information(upc, storeId, db):
    all_time_dataframe = allTimeDataframe(storeId, upc, db=db)
    itemGeneralInformation = ItemGeneralInformation()
    if len(all_time_dataframe) > 0:
        currentDate = datetime.today()
        sevenDaysAgo = currentDate - timedelta(days=7)
        sevenDayPriceChangeObject = calculatePriceChangeDays(all_time_dataframe, sevenDaysAgo, currentDate)
        itemGeneralInformation.price7DaysAgo = sevenDayPriceChangeObject["firstPrice"]
        itemGeneralInformation.price = sevenDayPriceChangeObject["lastPrice"]
        itemGeneralInformation.percentPriceChange7Days = sevenDayPriceChangeObject["percentPriceChange"]
        itemGeneralInformation.priceChangeLast7Days = sevenDayPriceChangeObject["priceChange"]

        thirtyDaysAgo = currentDate - timedelta(days=30)
        thirtyDayPriceChangeObject = calculatePriceChangeDays(all_time_dataframe, thirtyDaysAgo, currentDate)
        itemGeneralInformation.price30DaysAgo = thirtyDayPriceChangeObject["firstPrice"]
        itemGeneralInformation.percentPriceChange30days = thirtyDayPriceChangeObject["percentPriceChange"]
        itemGeneralInformation.priceChangeLast30days = thirtyDayPriceChangeObject["priceChange"]

        itemGeneralInformation.earliestPrice = SafewayItem.parse_obj(all_time_dataframe[0]).price
        itemGeneralInformation.priceChangeForAllRecords = itemGeneralInformation.earliestPrice - itemGeneralInformation.price
        itemGeneralInformation.percentPriceChangeForAllRecords = float('{:0.2f}'.format((
                                                                                                itemGeneralInformation.priceChangeForAllRecords / itemGeneralInformation.earliestPrice) * 100))

    fillOutGeneralInformation(itemGeneralInformation, storeId, upc, db=db)
    fillOut5ItemsInCategory(currentItemGeneralInformation=itemGeneralInformation, storeId=storeId, db=db)
    # print(itemGeneralInformation.__dict__)
    return itemGeneralInformation.__dict__
    # price 10 items
    # price change 10 items


def getDataFrameJsonObject(storeId, upc, days_before, db) -> list[SafewayItemDBModel]:
    days_before = datetime.today() - timedelta(days=7)
    query = db.query(SafewayItemDBModel.name, SafewayItemDBModel.upc, SafewayItemDBModel.date,
                     SafewayItemDBModel.price,
                     SafewayItemDBModel.basePrice, SafewayItemDBModel.pricePer).filter(and_(
        SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc,
        SafewayItemDBModel.date > days_before)).order_by(
        asc(SafewayItemDBModel.date))
    df = pandas.read_sql_query(query.statement, con=RDSConnection.get_engine())

    jsonResponse = json.loads(df.to_json(orient='records'))
    newJsonResponse = []
    for entry in jsonResponse:
        currentDate = datetime.fromtimestamp(int(entry['date'] / 1000))
        entry['date'] = currentDate.strftime("%Y-%m-%d")
        newJsonResponse.append(entry)
    return newJsonResponse


def allTimeDataframe(storeId, upc, db):
    query = db.query(SafewayItemDBModel.name, SafewayItemDBModel.upc, SafewayItemDBModel.date,
                     SafewayItemDBModel.price,
                     SafewayItemDBModel.basePrice, SafewayItemDBModel.pricePer).filter(and_(
        SafewayItemDBModel.storeId == storeId, SafewayItemDBModel.upc == upc)).order_by(
        asc(SafewayItemDBModel.date))
    df = pandas.read_sql_query(query.statement, con=RDSConnection.get_engine())
    jsonResponse = json.loads(df.to_json(orient='records'))
    newJsonResponse = []
    for entry in jsonResponse:
        currentDate = datetime.fromtimestamp(int(entry['date'] / 1000))
        entry['date'] = currentDate.strftime("%Y-%m-%d")
        newJsonResponse.append(entry)
    return newJsonResponse


def calculatePriceChangeDays(dataFrameJsonObject: list[SafewayItemDBModel], startDate, endDate):
    indexOfStartDate = findIndex(dataFrameJsonObject, startDate.date())
    indexOfEndDate = findIndex(dataFrameJsonObject, endDate.date())
    first = SafewayItem.parse_obj(dataFrameJsonObject[indexOfStartDate])
    last = SafewayItem.parse_obj(dataFrameJsonObject[indexOfEndDate])

    priceChange = float('{:0.2f}'.format(last.price - first.price))
    percentPriceChange = float('{:0.2f}'.format((priceChange / first.price) * 100))
    return {
        "startDate": first.date,
        "endDate": last.date,
        "firstPrice": first.price,
        "lastPrice": last.price,
        "priceChange": priceChange,
        "percentPriceChange": percentPriceChange
    }


def findIndex(data_frame_json_array, date_looking_for):
    data_frame_dates = []
    for json_object in data_frame_json_array:
        data_frame_dates.append(SafewayItem.parse_obj(json_object).date)

    index = bisect_left(data_frame_dates, date_looking_for)
    if index == len(data_frame_dates):
        return index - 1
    elif index:
        return index
    else:
        return 0

# general_info = build_general_information("0027680300000", "2948", get_postgres_session())
# print(json.dumps(general_info, default=str))
