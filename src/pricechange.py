from uuid import uuid4

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItems
from grocerywebcrawler.rds_connection import RDSConnection
from webserver.largest_price_changes import createPriceChangeObjects

if __name__ == '__main__':
    createPriceChangeObjects()

    # db = get_normal_session()
    # all_price_changes: List[PriceChangeDBModel] = db.query(PriceChangeDBModel).all()
    # for price_change in all_price_changes:
    #     db.query(PriceChangeDBModel).filter(PriceChangeDBModel.id == price_change.id).update({
    #         PriceChangeDBModel.absPercentPriceChange7Days: abs(price_change.percentPriceChange7DaysAgo),
    #         PriceChangeDBModel.absPercentPriceChange30Days: abs(price_change.percentPriceChange30Days)
    #     })
    # db.commit()

    # db = RDSConnection.get_normal_session()
    # all_distinct_items = db.query(DistinctSafewayItem).all()
    # for index, item in enumerate(all_distinct_items):
    #     try:
    #         existing = db.query(DistinctSafewayItems).filter(and_(DistinctSafewayItems.upc==item.upc, DistinctSafewayItems.storeId==item.storeId)).one()
    #     except NoResultFound:
    #         migratedItem = DistinctSafewayItems(id=uuid4(), upc=item.upc, storeId=item.storeId, name=item.name,
    #                                     departmentName=item.departmentName, date=item.date, area=item.area,
    #                                     storesAvailable=None)
    #         db.add(migratedItem)
    #     if index%100==0:
    #         db.commit()
    # db.commit()
