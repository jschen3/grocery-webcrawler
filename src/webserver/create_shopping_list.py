import datetime
from typing import Optional

from pydantic.main import BaseModel

from webserver.models.shopping_list_item import ShoppingListItem
from webserver.price_comparison_between_stores import create_price_comparison_between_stores, \
    PriceComparisonBetweenStores


class PriceAtStore(BaseModel):
    index: Optional[int]
    upc: Optional[str]
    name: Optional[str]
    storeId: Optional[str]
    storeLocation: Optional[str]
    price: Optional[float]
    updatedDate: Optional[datetime.date]


class GroupedStoreAndItems(BaseModel):
    storeId: Optional[str]
    storeLocation: Optional[str]
    shoppingItems: Optional[list[PriceAtStore]]
    totalPrice: Optional[float]
    missingItems: Optional[list[str]]


class ShoppingListOutput(BaseModel):
    shoppingListItems: Optional[list[ShoppingListItem]]
    optimalStore: Optional[GroupedStoreAndItems]


def create_shopping_list_output(shoppingList, db):
    priceAtStores = []
    stores = set()
    shoppingListItemsList = []
    for index, upc in enumerate(shoppingList):
        priceComparisonObject: PriceComparisonBetweenStores = create_price_comparison_between_stores(upc, db)
        highestPrice = 0.0
        highestPriceLocation = None
        lowestPrice = 1000000
        lowestPriceLocation = None
        lowestDate = None
        # fix bug not every item has multiple price objects here...
        for price in priceComparisonObject.prices:
            newPriceAtStore = PriceAtStore(index=index, upc=priceComparisonObject.upc, name=priceComparisonObject.name,
                                           storeLocation=price.storeLocation, price=price.price, storeId=price.storeId,
                                           updatedDate=price.date)
            priceAtStores.append(newPriceAtStore)
            if price.price > highestPrice:
                highestPrice = price.price
                highestPriceLocation = price.storeLocation
            if price.price < lowestPrice:
                lowestPrice = price.price
                lowestPriceLocation = price.storeLocation
                lowestDate = price.date
            stores.add(price.storeId)
        shoppingListItem = ShoppingListItem(index=index, updatedDate=lowestDate, itemName=priceComparisonObject.name,
                                            upc=upc,
                                            cheapestPrice=lowestPrice, cheapestPriceLocation=lowestPriceLocation,
                                            highestPrice=highestPrice, highestPriceLocation=highestPriceLocation)
        shoppingListItemsList.append(shoppingListItem)
    storeToGroupedItems = {}
    storeItems = []
    for priceAtStore in priceAtStores:
        store = priceAtStore.storeId
        if store in storeToGroupedItems:
            storeToGroupedItems[store].append(priceAtStore)
        else:
            storeToGroupedItems[store] = []
            storeToGroupedItems[store].append(priceAtStore)
    for store in storeToGroupedItems.keys():
        itemsAtStore = storeToGroupedItems[store]
        items = set()
        price = 0
        for item in itemsAtStore:
            items.add(item.upc)
            price += item.price
        missingItems = []
        for origItem in shoppingList:
            if origItem not in items:
                missingItems.append(origItem)

        group = GroupedStoreAndItems(storeId=store, shoppingItems=itemsAtStore, totalPrice=price,
                                     missingItems=missingItems)
        group.storeLocation = itemsAtStore[0].storeLocation # may be buggy
        storeItems.append(group)

    optimalStoreGroup = None
    lowestPrice = 1000000
    for groupedStoreAndItems in storeItems:
        if groupedStoreAndItems.totalPrice < lowestPrice and len(groupedStoreAndItems.missingItems) == 0:
            lowestPrice = groupedStoreAndItems.totalPrice
            optimalStoreGroup = groupedStoreAndItems

    shoppinglistOutput = ShoppingListOutput()
    shoppinglistOutput.shoppingListItems = shoppingListItemsList
    shoppinglistOutput.optimalStore = optimalStoreGroup
    return shoppinglistOutput
