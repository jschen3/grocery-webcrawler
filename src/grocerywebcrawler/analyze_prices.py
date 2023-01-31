import csv
import json
from typing import List

from grocerywebcrawler.models.price_comparison_object import PriceComparisonObject, PriceAttributes
from grocerywebcrawler.models.safeway_item import SafewayItem


def mostSignificantPriceChanges(path1, path2):
    file1Items = fileItems(path1)
    file2Items = fileItems(path2)
    priceChanges = []
    for item in file1Items:
        upc = item.upc
        priceAttribute1 = getPriceAttributes(upc, file1Items)
        priceAttribute2 = getPriceAttributes(upc, file2Items)
        if priceAttribute1 is not None and priceAttribute2 is not None:
            priceChanges.append(comparePriceAttributes(priceAttribute1, priceAttribute2))
    sortedPriceChanges = sorted(priceChanges, key=lambda x: x.percentageChangePrice, reverse=True)
    return sortedPriceChanges[0:100]


def readablePriceChanges(priceChanges: list[PriceComparisonObject]):
    for priceChange in priceChanges:
        print(
            f"name: {priceChange.name}  percentageChangePrice: {priceChange.percentageChangePrice}  priceChange: {priceChange.priceChange}  price1: {priceChange.price1}  price2: {priceChange.price2}")


def fileItems(file) -> List[SafewayItem]:
    items = []
    with open(file, "r") as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            averageWeight = line["averageWeight"]
            # channelInventory = line["channelInventory"]
            if "averageWeight" in line:
                del line["averageWeight"]
            if "channelInventory" in line:
                del line["channelInventory"]
            pricePer = line["pricePer"]
            try:
                line["pricePer"] = float(line["pricePer"])
            except:
                line["pricePer"] = None
            items.append(SafewayItem.parse_obj(line))
        return items


def jsonItems(file, outpath, start, limit):
    items = []
    json_file = []
    with open(file, "r") as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            averageWeight = line["averageWeight"]
            # channelInventory = line["channelInventory"]
            if "averageWeight" in line:
                del line["averageWeight"]
            if "channelInventory" in line:
                del line["channelInventory"]
            pricePer = line["pricePer"]
            try:
                line["pricePer"] = float(line["pricePer"])
            except:
                line["pricePer"] = None
            single_item = SafewayItem.parse_obj(line)

            items.append(single_item)
            json_file.append(single_item.dict())
        with open(outpath, "w") as outfile:
            outfile.write(json.dumps(json_file[start:start + limit]))


def getPriceAttributes(upc, listOfItems: List[SafewayItem]):
    for singleItem in listOfItems:
        if singleItem.upc == upc:
            priceAttributes = PriceAttributes(upc=singleItem.upc, name=singleItem.name, price=singleItem.price,
                                              basePrice=singleItem.basePrice, pricePer=singleItem.pricePer,
                                              unitQuantity=singleItem.unitQuantity,
                                              averageWeight=singleItem.averageWeight)
            return priceAttributes
    return None


def comparePriceAttributes(priceAttribute1: PriceAttributes, priceAttribute2: PriceAttributes):
    basePriceChange = None
    percentageChangeBasePrice = None
    priceChange = None
    percentageChangePrice = None
    pricePerChange = None
    percentageChangePricePer = None

    if priceAttribute1.price != None and priceAttribute2.price != None:
        basePriceChange = priceAttribute2.basePrice - priceAttribute1.basePrice
        percentageChangeBasePrice = (basePriceChange / priceAttribute2.basePrice) * 100

    if priceAttribute1.price != None and priceAttribute2.price != None:
        priceChange = priceAttribute2.price - priceAttribute1.price
        percentageChangePrice = (priceChange / priceAttribute2.price) * 100

    if priceAttribute1.pricePer != None and priceAttribute2.pricePer != None and priceAttribute2.pricePer != 0.0:
        pricePerChange = priceAttribute2.pricePer - priceAttribute2.pricePer
        percentageChangePricePer = (pricePerChange / priceAttribute2.pricePer) * 100

    return PriceComparisonObject(name=priceAttribute2.name, upc=priceAttribute2.upc, basePriceChange=basePriceChange,
                                 percentageChangeBasePrice=percentageChangeBasePrice,
                                 priceChange=priceChange, percentageChangePrice=percentageChangePrice,
                                 pricePerChange=pricePerChange, percentageChangePricePer=percentageChangePricePer,
                                 price1=priceAttribute1.price,
                                 price2=priceAttribute2.price)


priceChanges = mostSignificantPriceChanges("safeway_csvs/safeway-store-2948-01-02-23.csv",
                                           "safeway_csvs/safeway-store-2948-12-22-22.csv")
readablePriceChanges(priceChanges)
# jsonItems("safeway_csvs/safeway-store-2948-12-22-22.csv", "safeway_jsons/safeway-store-2948-12-22-22.json", 0, 100)
