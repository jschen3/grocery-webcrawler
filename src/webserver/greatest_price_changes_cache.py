from datetime import date, timedelta, datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from webserver.models.price_change_object import PriceChangeDBModel


class GreatestPriceChangesCache:
    __store_30day_price_change = {}
    __store_7day_price_change = {}

    @staticmethod
    def get_greatest_price_changes(storeId: str, thirtyOr7Days: bool, limit: int, offset: int, db: Session):
        date_string = '2023-08-09'
        august_date = datetime.strptime(date_string, "%Y-%m-%d")
        thirty_days_ago = august_date - timedelta(
            days=1)
        one_week_ago = august_date - timedelta(days=1)
        if limit != 50 and offset != 0:
            # true = thirtydays
            # false = 7 days
            if thirtyOr7Days:
                return db.query(PriceChangeDBModel.upc,
                                                     PriceChangeDBModel.name,
                                                     PriceChangeDBModel.storeId,
                                                     PriceChangeDBModel.category,
                                                     PriceChangeDBModel.price7DaysAgo,
                                                     PriceChangeDBModel.price30DaysAgo,
                                                     PriceChangeDBModel.currentPrice,
                                                     PriceChangeDBModel.priceChange7DaysAgo,
                                                     PriceChangeDBModel.priceChange30Days,
                                                     PriceChangeDBModel.percentPriceChange7DaysAgo,
                                                     PriceChangeDBModel.percentPriceChange30Days,
                                                     PriceChangeDBModel.absPercentPriceChange7Days,
                                                     PriceChangeDBModel.absPercentPriceChange30Days,
                                                     PriceChangeDBModel.currentDate).filter(and_(
                        PriceChangeDBModel.currentDate > thirty_days_ago,
                        PriceChangeDBModel.storeId == storeId)).order_by(
                        PriceChangeDBModel.absPercentPriceChange30Days.desc()).limit(
                        limit * 10).offset(offset).all()
            else:
                return db.query(PriceChangeDBModel.upc,
                                PriceChangeDBModel.name,
                                PriceChangeDBModel.storeId,
                                PriceChangeDBModel.category,
                                PriceChangeDBModel.price7DaysAgo,
                                PriceChangeDBModel.price30DaysAgo,
                                PriceChangeDBModel.currentPrice,
                                PriceChangeDBModel.priceChange7DaysAgo,
                                PriceChangeDBModel.priceChange30Days,
                                PriceChangeDBModel.percentPriceChange7DaysAgo,
                                PriceChangeDBModel.percentPriceChange30Days,
                                PriceChangeDBModel.absPercentPriceChange7Days,
                                PriceChangeDBModel.absPercentPriceChange30Days,
                                PriceChangeDBModel.currentDate).filter(and_(
                    PriceChangeDBModel.currentDate > one_week_ago, PriceChangeDBModel.storeId == storeId)).order_by(
                    PriceChangeDBModel.absPercentPriceChange7Days.desc()).limit(
                    limit*10).offset(offset).all()
        else:
            if thirtyOr7Days:
                if storeId in GreatestPriceChangesCache.__store_30day_price_change:
                    return GreatestPriceChangesCache.__store_30day_price_change[storeId]
                else:
                    thirty_day_db_request = db.query(PriceChangeDBModel.upc,
                                                     PriceChangeDBModel.name,
                                                     PriceChangeDBModel.storeId,
                                                     PriceChangeDBModel.category,
                                                     PriceChangeDBModel.price7DaysAgo,
                                                     PriceChangeDBModel.price30DaysAgo,
                                                     PriceChangeDBModel.currentPrice,
                                                     PriceChangeDBModel.priceChange7DaysAgo,
                                                     PriceChangeDBModel.priceChange30Days,
                                                     PriceChangeDBModel.percentPriceChange7DaysAgo,
                                                     PriceChangeDBModel.percentPriceChange30Days,
                                                     PriceChangeDBModel.absPercentPriceChange7Days,
                                                     PriceChangeDBModel.absPercentPriceChange30Days,
                                                     PriceChangeDBModel.currentDate).filter(and_(
                        PriceChangeDBModel.currentDate > thirty_days_ago,
                        PriceChangeDBModel.storeId == storeId)).order_by(
                        PriceChangeDBModel.absPercentPriceChange30Days.desc()).limit(
                        limit * 10).offset(offset).all()
                    GreatestPriceChangesCache.__store_30day_price_change[storeId] = thirty_day_db_request
                    return GreatestPriceChangesCache.__store_30day_price_change[storeId]
            else:
                if storeId in GreatestPriceChangesCache.__store_7day_price_change:
                    return GreatestPriceChangesCache.__store_7day_price_change[storeId]
                else:
                    seven_day_db_request = db.query(PriceChangeDBModel.upc,
                                                    PriceChangeDBModel.name,
                                                    PriceChangeDBModel.storeId,
                                                    PriceChangeDBModel.category,
                                                    PriceChangeDBModel.price7DaysAgo,
                                                    PriceChangeDBModel.price30DaysAgo,
                                                    PriceChangeDBModel.currentPrice,
                                                    PriceChangeDBModel.priceChange7DaysAgo,
                                                    PriceChangeDBModel.priceChange30Days,
                                                    PriceChangeDBModel.percentPriceChange7DaysAgo,
                                                    PriceChangeDBModel.percentPriceChange30Days,
                                                    PriceChangeDBModel.absPercentPriceChange7Days,
                                                    PriceChangeDBModel.absPercentPriceChange30Days,
                                                    PriceChangeDBModel.currentDate).filter(and_(
                        PriceChangeDBModel.currentDate > one_week_ago, PriceChangeDBModel.storeId == storeId)).order_by(
                        PriceChangeDBModel.absPercentPriceChange7Days.desc()).limit(
                        limit * 10).offset(offset).all()
                    GreatestPriceChangesCache.__store_7day_price_change[storeId] = seven_day_db_request
                    return GreatestPriceChangesCache.__store_7day_price_change[storeId]

    @staticmethod
    def clear_cache():
        GreatestPriceChangesCache.__store_30day_price_change = {}
        GreatestPriceChangesCache.__store_7day_price_change = {}
