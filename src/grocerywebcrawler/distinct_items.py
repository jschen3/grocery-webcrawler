from grocerywebcrawler.models.distinct_safeway_items import DistinctSafewayItem
from grocerywebcrawler.models.safeway_item import SafewayItemDBModel
from grocerywebcrawler.rds_connection import get_postgres_session, get_engine


def distinct_items():
    session = get_postgres_session()
    distinct_items: list[SafewayItemDBModel] = session.query(SafewayItemDBModel).distinct(SafewayItemDBModel.upc).all()
    for distinct_item in distinct_items:
        distinct = DistinctSafewayItem(upc=distinct_item.upc, storeId=distinct_item.storeId,
                                       name=distinct_item.name,
                                       departmentName=distinct_item.departmentName, date=distinct_item.date,
                                       area=distinct_item.area)
        try:
            existingDistinct = session.query(DistinctSafewayItem).where(
                distinct.upc == DistinctSafewayItem.upc).one()
        except:
            session.add(distinct)
    session.commit()


distinct_items()
