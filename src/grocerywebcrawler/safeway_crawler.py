import csv
import json
from datetime import date
import os
from time import sleep

import requests

from grocerywebcrawler.models.safeway_item import SafewayItem, SafewayItemDBModel
from grocerywebcrawler.headless_browser_util import headless_browser_request_id
from grocerywebcrawler.rds_connection import get_normal_session

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem


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
    doc_models = []
    next_parameters = request_parameters.copy()
    session = get_normal_session()
    for i in range(0, num_found, 30):
        next_parameters["start"] = i
        try:
            response = requests.get(url=url, params=next_parameters, headers=headers)
            if response.status_code == 204 or response.status_code == 429:
                print(f"{response.reason}")
                break
            json_response = requests.get(url=url, params=next_parameters, headers=headers).json()["response"]
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
                        doc_models.append(doc_model)
                    except Exception as e:
                        print(e)
                        print(f"unable to process json_doc:{json_doc[1]}")
                        continue

            else:
                new_request_id = headless_browser_request_id()
                next_parameters["request-id"] = new_request_id
                continue
        except Exception as e:
            # print(response.content)
            print(e)
            print(f"an error occurred processing items. i={i} out of num_found={num_found} counter={counter}")
            continue
        session.commit()
        print(f"looped through and created safeway items. Committed items. Current at {i} out of {num_found}")
        sleep(0.25)
    print(f"finished items at store: {storeid}")
    return doc_models


def _write_excel_file(doc_models, storeid):
    dirname = os.path.dirname(__file__)
    safeway_date_file = f"safeway-store-{storeid}-{date.today().strftime('%m-%d-%y')}.csv"
    relative_path = os.path.join(dirname, f"safeway_csvs/{safeway_date_file}")

    fieldnames = SafewayItem.__fields__.keys()
    with open(relative_path, "w") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for safeway_doc in doc_models:
            writer.writerow(json.loads(safeway_doc.json()))

    print(f"wrote csv file. All items in csv file. {safeway_date_file}")

# write_excel_file(doc_models, 2948)
# https://pybit.es/articles/how-to-package-and-deploy-cli-apps/
