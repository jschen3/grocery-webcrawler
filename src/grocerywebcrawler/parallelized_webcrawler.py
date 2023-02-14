import math
import multiprocessing
import traceback
from datetime import date, datetime
from time import sleep

import requests
from sqlalchemy.exc import NoResultFound

from grocerywebcrawler.models.safeway_item import SafewayItem, SafewayItemDBModel
from grocerywebcrawler.headless_browser_util import headless_browser_request_id

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from grocerywebcrawler.rds_connection import RDSConnection
from util.logging import info
from webserver.models.operation_db_model import OperationDbModel


def _safeway_items_from_json(json_doc: dict, store_id: str, date: date, area: str, storeType: str) -> SafewayItem:
    pricePer = json_doc["pricePer"] if "pricePer" in json_doc else None
    averageWeightList = json_doc["averageWeight"] if "averageWeight" in json_doc else None
    if isinstance(averageWeightList, list):
        averageWeight = averageWeightList[0]
    else:
        averageWeight = averageWeightList
    unitQuantity = json_doc["unitQuantity"] if "unitQuantity" in json_doc else None
    unitOfMeasure = json_doc["unitOfMeasure"] if "unitOfMeasure" in json_doc else None
    channelInventory = json_doc["channelInventory"] if "channelInventory" in json_doc else None
    promoDescription = json_doc["promoDescription"] if "promoDescription" in json_doc else None
    name = json_doc["name"] if "name" in json_doc else None

    safeway_item = SafewayItem(name=name, upc=json_doc["upc"], price=json_doc["price"],
                               basePrice=json_doc["basePrice"],
                               pricePer=pricePer, averageWeight=averageWeight,
                               unitQuantity=unitQuantity,
                               departmentName=json_doc["departmentName"], salesRank=json_doc["salesRank"],
                               unitOfMeasure=unitOfMeasure, inventoryAvailable=json_doc["inventoryAvailable"],
                               channelInventory=channelInventory, promoDescription=promoDescription, storeId=store_id,
                               date=date, area=area, storeType=storeType)
    safeway_item.upc_date_store_id = f"{safeway_item.upc}_{date}_{store_id}"
    return safeway_item


def get_all_safeway_items_from_store(storeid):
    request_parameters = {
        "request-id": 2051668903794860761,
        "rows": 30,
        "start": 0,
        "storeid": storeid
    }

    headers = {
        "ocp-apim-subscription-key": "e914eec9448c4d5eb672debf5011cf8f"
    }
    url = "https://www.safeway.com/abs/pub/xapi/search/products?url=https://www.safeway.com&pageurl=https://www.safeway" \
          ".com&pagename=search&search-type=keyword&search-uid=uid%253D5224296067385%253Av%253D12.0%253Ats" \
          "%253D1668295333830%253Ahc%253D18&q=&sort=&dvid=web-4.1search&channel=instore"
    request_id = headless_browser_request_id()
    request_parameters["request-id"] = request_id
    first_response = requests.get(url=url, params=request_parameters, headers=headers).json()["response"]
    num_found = first_response["numFound"]
    print(f"Initial request performed. Total number of items at store: {storeid} num_found: {num_found}")
    info(f"Initial request performed. Total number of items at store: {storeid} num_found: {num_found}")
    next_parameters = request_parameters.copy()
    session = RDSConnection.get_normal_session()
    try:
        existing = session.query(OperationDbModel).filter(
            OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").one()
        session.query(OperationDbModel).filter(
            OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").update(
            {OperationDbModel.count: existing.count + 1, OperationDbModel.date: date.today()})
        session.commit()
    except NoResultFound:
        operationsRecord = OperationDbModel(id=f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}",
                                            operationName="webcrawl", date=date.today(), totalItems=num_found,
                                            currentProcessed=0, storeId=storeid, status="Started", count=0)
        session.add(operationsRecord)
        session.commit()
    ranges = []
    for i in range(0, math.ceil(num_found/4), 30):
        ranges.append((i, storeid, num_found))
    try:
        pool_obj = multiprocessing.Pool()
        pool_obj.map(loop, ranges)
    except Exception:
        print(f"An exception occurred {traceback.format_exc()}")
        info(f"An exception occurred {traceback.format_exc()}")
    session.query(OperationDbModel).filter(
        OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").update(
        {OperationDbModel.status: "Finished",
         OperationDbModel.date: date.today()})
    session.commit()
    print(f"finished items at store: {storeid}")
    info(f"finished items at store: {storeid}")

# write_excel_file(doc_models, 2948)
# https://pybit.es/articles/how-to-package-and-deploy-cli-apps/

def loop(ranges):
    start = ranges[0]
    storeid = ranges[1]
    num_found = ranges[2]
    session = RDSConnection.get_postgres_session()
    request_parameters = {
        "request-id": 2051668903794860761,
        "rows": 30,
        "start": 0,
        "storeid": storeid
    }
    headers = {
        "ocp-apim-subscription-key": "e914eec9448c4d5eb672debf5011cf8f"
    }
    url = "https://www.safeway.com/abs/pub/xapi/search/products?url=https://www.safeway.com&pageurl=https://www.safeway" \
          ".com&pagename=search&search-type=keyword&search-uid=uid%253D5224296067385%253Av%253D12.0%253Ats" \
          "%253D1668295333830%253Ahc%253D18&q=&sort=&dvid=web-4.1search&channel=instore"
    request_id = headless_browser_request_id()
    request_parameters["request-id"] = request_id
    request_parameters["start"] = start
    try:
        response = requests.get(url=url, params=request_parameters, headers=headers)
        if response.status_code == 204 or response.status_code == 429:
            print(f"{response.reason}")
            info(f"{response.reason}")
            return
        json_response = requests.get(url=url, params=request_parameters, headers=headers).json()["response"]
        counter = 0
        if json_response is not None:
            docs = json_response["docs"]
            for json_doc in enumerate(docs):
                counter = json_doc[0]
                try:
                    doc_model = _safeway_items_from_json(json_doc[1], store_id=storeid, date=date.today(),
                                                         area="bay-area", storeType="safeway")
                    safeway_item_dbmodel = doc_model.to_db_model()
                    try:
                        existing_item = session.query(SafewayItemDBModel).where(
                            SafewayItemDBModel.id == safeway_item_dbmodel.id).one()
                    except:
                        session.add(safeway_item_dbmodel)
                    try:
                        existingDistinct = session.query(DistinctSafewayItem).where(
                            safeway_item_dbmodel.upc == DistinctSafewayItem.upc).one()
                    except:
                        distinct = DistinctSafewayItem(upc=safeway_item_dbmodel.upc,
                                                       storeId=safeway_item_dbmodel.storeId,
                                                       name=safeway_item_dbmodel.name,
                                                       departmentName=safeway_item_dbmodel.departmentName,
                                                       date=safeway_item_dbmodel.date,
                                                       area=safeway_item_dbmodel.area)
                        try:
                            session.add(distinct)
                        except:
                            session.rollback()
                            raise
                except Exception as e:
                    print(e)
                    info(e)
                    print(f"unable to process json_doc:{json_doc[1]}")
                    info(f"unable to process json_doc:{json_doc[1]}")
                    return
        else:
            new_request_id = headless_browser_request_id()
            request_parameters["request-id"] = new_request_id
            return
    except Exception as e:
        print(e)
        info(e)
        print(f"an error occurred processing items. i={start} out of num_found={num_found} counter={counter}")
        info(f"an error occurred processing items. i={start} out of num_found={num_found} counter={counter}")
        return
    session.commit()
    # if i % 300 == 0:
    #     session.query(OperationDbModel).filter(
    #         OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").update({
    #         OperationDbModel.currentProcessed: i, OperationDbModel.status: "Processing"
    #     })
    #     session.commit()
    print(f"looped through and created safeway items. Committed items. Current at {start} out of {num_found}")
    info(f"looped through and created safeway items. Committed items. Current at {start} out of {num_found}")
    sleep(.25)



