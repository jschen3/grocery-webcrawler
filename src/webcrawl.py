import time

from grocerywebcrawler.safeway_crawler import get_all_safeway_items_from_store
from webserver.LargestPriceChanges import createPriceChangeObjects

if __name__ == '__main__':
    safeway_items = get_all_safeway_items_from_store(2948)
    time.sleep(300)
    createPriceChangeObjects()