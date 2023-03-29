import traceback
import uuid
from datetime import date, datetime
import requests
from sqlalchemy import and_

from grocerywebcrawler.models.safeway_item import SafewayItem, SafewayItemDBModel
from grocerywebcrawler.headless_browser_util import headless_browser_request_id

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItems
from grocerywebcrawler.proxy_util import ProxyUtil
from grocerywebcrawler.rds_connection import RDSConnection
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
    request_id = headless_browser_request_id()
    prevRequestId = request_id["request-id"]
    prevOcpKey = request_id["ocp-apim-subscription-key"]
    response = makeRestRequest(prevRequestId, prevOcpKey, 0, storeid)
    print(response)
    num_found = response["numFound"]
    print(f"Initial request performed. Total number of items at store: {num_found}  storeid: {storeid}")
    session = RDSConnection.get_normal_session()
    current_count = session.query(SafewayItemDBModel).count()
    record_count = session.query(OperationDbModel).count()
    countToday = session.query(OperationDbModel).filter(OperationDbModel.date >= date.today()).count()
    operationsRecord = OperationDbModel(id=f"webcrawl_{datetime.today()}_{storeid}",
                                        operationName="webcrawl", date=datetime.now(), totalItems=current_count,
                                        newItems=0, prevItemCount=current_count, intId=record_count + 1,
                                        storeId=storeid, status="started", countToday=countToday + 1)
    session.add(operationsRecord)
    session.commit()
    try:
        for i in range(0, num_found, 30):
            json_response = makeRestRequest(prevRequestId, prevOcpKey, i, 2948)
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
                            existingDistinct = session.query(DistinctSafewayItems).where(and_(
                                safeway_item_dbmodel.upc == DistinctSafewayItems.upc,
                                DistinctSafewayItems.storeId == safeway_item_dbmodel.storeId)).one()
                        except:
                            distinct = DistinctSafewayItems(id=uuid.uuid4(), upc=safeway_item_dbmodel.upc,
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
                        print(f"unable to process json_doc:{json_doc[1]}")
                        continue
            session.commit()
            # if i % 300 == 0:
            #     session.query(OperationDbModel).filter(
            #         OperationDbModel.id == f"webcrawl_{datetime.today().strftime('%Y-%m-%d')}_{storeid}").update({
            #         OperationDbModel.currentProcessed: i, OperationDbModel.status: "Processing"
            #     })
            #     session.commit()
            print(f"looped through and created safeway items. Committed items. Current at {i} out of {num_found}")
            # sleep(0.25)
    except Exception:
        print("loop failed unable to go through all items")
    print(f"finished items at store: {storeid}")
    newCountToday = session.query(OperationDbModel).filter(OperationDbModel.date >= date.today()).count()
    newIntId = session.query(OperationDbModel).count()
    new_count = session.query(SafewayItemDBModel).count()
    finishedOperationRecord = OperationDbModel(id=f"webcrawl_{datetime.today()}_{storeid}",
                                               operationName="webcrawl", date=datetime.now(),
                                               newItems=new_count - current_count, prevItemCount=current_count,
                                               totalItems=new_count,
                                               storeId=storeid, status="finished", countToday=newCountToday + 1,
                                               intId=newIntId + 1, itemsCrawled=i)
    session.add(finishedOperationRecord)
    session.commit()
    print(
        f"webcrawled store {storeid} | original count: {current_count} | new count: {new_count - current_count} | total count: {new_count} items_crawled: {i}")


def makeRestRequest(prevRequestId: str, prevOcpKey: str, start: int, storeId: int):
    request_parameters = {'request-id': '3621677258217438273', 'rows': '30',
                          'start': '0', 'storeid': '2948'}
    headers = {
        "Ocp-Apim-Subscription-Key": "e914eec9448c4d5eb672debf5011cf8f",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/110.0.5481.177 Safari/537.36",
        "Referer": "https://www.safeway.com/shop/deals/member-specials.html",
        "Connection": "keep-alive",
        "sec-ch-ua": "", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": ""
    }
    url = "https://www.safeway.com/abs/pub/xapi/search/products?url=https://www.safeway.com&pageurl=https://www.safeway.com&pagename=search&search-type=keyword&featured=false&search-uid=&q=&sort=&userid=&featuredsessionid=&screenwidth=800,600&dvid=web-4.1search&channel=instore&banner=safeway&fq=promoType:%22P%22&fq=instoreInventory:%221%22"
    request_parameters["request-id"] = prevRequestId
    request_parameters["storeid"] = storeId
    request_parameters["start"] = start
    headers["Ocp-Apim-Subscription-Key"] = prevOcpKey
    # proxy = ProxyUtil.getProxy()
    attempts = 0
    while attempts < 40:
        try:
            # print(proxy)
            response = make_http_request(url=url, params=request_parameters, headers=headers, use_proxy=False)
            status = response.status_code
            if status == 200:
                return response.json()["response"]
            else:
                print(f"Response not 200. Incrementing proxy. {response.status_code} response: {response.text}")
                ProxyUtil.increment(ProxyUtil.getProxy())
                request_ids = headless_browser_request_id()
                headers["Ocp-Apim-Subscription-Key"] = request_ids["ocp-apim-subscription-key"]
                request_parameters["request_id"] = request_ids["request-id"]
                attempts += 1
                continue
        except Exception as e:
            ProxyUtil.increment(ProxyUtil.getProxy())
            attempts += 1
            request_ids = headless_browser_request_id()
            headers["Ocp-Apim-Subscription-Key"] = request_ids["ocp-apim-subscription-key"]
            request_parameters["request_id"] = request_ids["request-id"]
            continue
    print(f"Unable to successively retrieve items from store. at start {start} storeid: {storeId}")
    raise Exception(f"Unable to successively retrieve items from store. at start {start} storeid: {storeId}")


def make_http_request(url, params, headers, use_proxy: bool):
    if use_proxy:
        proxy = ProxyUtil.getProxy()
        print(f"proxy: {proxy}")
        try:
            response = requests.get(url, proxies=proxy, params=params, headers=headers, timeout=5)
        except Exception as e:
            print(proxy)
            print(e)
            raise e
        return response
    else:
        return requests.get(url, params=params, headers=headers, timeout=5)
