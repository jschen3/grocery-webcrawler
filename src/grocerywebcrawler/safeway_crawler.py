import json
from datetime import date, datetime
from json import JSONDecodeError

import requests
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
    print("Starting webcrawling.")
    info("Starting webcrawling.")
    request_parameters = {'request-id': '3621677258217438273', 'rows': '30',
                          'start': '0', 'storeid': '3132'}

    headers = {
        "Ocp-Apim-Subscription-Key": "e914eec9448c4d5eb672debf5011cf8f",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/110.0.5481.177 Safari/537.36",
        "Referer": "https://www.safeway.com/shop/deals/member-specials.html",
        "Connection": "keep-alive",
        "sec-ch-ua": "", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": ""
    }
    url = "https://www.safeway.com/abs/pub/xapi/search/products?request-id=3301677259115566322&url=https://www.safeway.com&pageurl=https://www.safeway.com&pagename=search&rows=30&start=0&search-type=keyword&storeid=3132&featured=false&search-uid=&q=&sort=&userid=&featuredsessionid=&screenwidth=800,600&dvid=web-4.1search&channel=instore&banner=safeway&fq=promoType:%22P%22&fq=instoreInventory:%221%22"
    request_id = headless_browser_request_id()
    request_parameters["request-id"] = request_id["request-id"]
    headers["ocp-apim-subscription-key"] = request_id["ocp-apim-subscription-key"]
    response = requests.get(url=url, params=request_parameters, headers=headers)
    response.raise_for_status()
    first_response = response.json()["response"]
    info(first_response)
    print(first_response)
    num_found = first_response["numFound"]
    print(f"Initial request performed. Total number of items at store: {storeid} num_found: {num_found}")
    info(f"Initial request performed. Total number of items at store: {storeid} num_found: {num_found}")
    next_parameters = request_parameters.copy()
    next_headers = headers.copy()
    session = RDSConnection.get_normal_session()
    current_count = session.query(SafewayItemDBModel).count()
    record_count = session.query(OperationDbModel).count()
    countToday = session.query(OperationDbModel).filter(OperationDbModel.date >= date.today()).count()
    operationsRecord = OperationDbModel(id=f"webcrawl_{datetime.today()}_{storeid}",
                                        operationName="webcrawl", date=date.today(), totalItems=current_count,
                                        newItems=0, prevItemCount=current_count, intId=record_count + 1,
                                        storeId=storeid, status="Started", countToday=countToday + 1)
    session.add(operationsRecord)
    session.commit()
    for i in range(0, num_found, 30):
        next_parameters["start"] = i
        try:
            response = requests.get(url=url, params=next_parameters, headers=next_headers)
            if response.status_code == 204 or response.status_code == 429:
                print(f"{response.reason}")
                info(f"{response.reason}")
                break
            json_response = requests.get(url=url, params=next_parameters, headers=next_headers).json()["response"]
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
                        continue

            else:
                new_request_id = headless_browser_request_id()
                next_parameters["request-id"] = new_request_id["request-id"]
                next_headers["ocp-apim-subscription-key"] = new_request_id["ocp-apim-subscription-key"]
                continue
        except Exception as e:
            print(e)
            info(e)
            print(f"an error occurred processing items. i={i} out of num_found={num_found} counter={counter}")
            info(f"an error occurred processing items. i={i} out of num_found={num_found} counter={counter}")
            continue
        session.commit()
        # if i % 300 == 0:
        #     session.query(OperationDbModel).filter(
        #         OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").update({
        #         OperationDbModel.currentProcessed: i, OperationDbModel.status: "Processing"
        #     })
        #     session.commit()
        print(f"looped through and created safeway items. Committed items. Current at {i} out of {num_found}")
        info(f"looped through and created safeway items. Committed items. Current at {i} out of {num_found}")
        # sleep(0.25)
    print(f"finished items at store: {storeid}")
    info(f"finished items at store: {storeid}")
    newCountToday = session.query(OperationDbModel).filter(OperationDbModel.date >= date.today()).count()
    newIntId = session.query(OperationDbModel).count()
    new_count = session.query(SafewayItemDBModel).count()
    finishedOperationRecord = OperationDbModel(id=f"webcrawl_{datetime.today()}_{storeid}",
                                               operationName="webcrawl", date=date.today(),
                                               newItems=new_count - current_count, prevItemCount=current_count,
                                               totalItems=new_count,
                                               storeId=storeid, status="Finished", countToday=newCountToday + 1,
                                               intId=newIntId + 1)
    session.add(finishedOperationRecord)
    session.commit()
    print(
        f"new items for store {storeid} | original count: {current_count} new count: {new_count - current_count} total count: {new_count}")
