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
