import time

from grocerywebcrawler.safeway_crawler import get_all_safeway_items_from_store

if __name__ == '__main__':
    safeway_items = get_all_safeway_items_from_store(2948)