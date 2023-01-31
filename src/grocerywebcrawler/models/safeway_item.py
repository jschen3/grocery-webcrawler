from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, TIMESTAMP, FLOAT, JSON
from sqlalchemy.orm import declarative_base
from datetime import date


class SafewayItem(BaseModel):
    name: Optional[str]
    upc: Optional[str]
    price: Optional[float]
    basePrice: Optional[float]
    pricePer: Optional[float]
    averageWeight: Optional[str]
    unitQuantity: Optional[str]
    departmentName: Optional[str]
    salesRank: Optional[str]
    unitOfMeasure: Optional[str]
    channelInventory: Optional[dict]
    inventoryAvailable: Optional[str]
    promoDescription: Optional[str]
    storeId: Optional[str]
    date: Optional[date]
    area: Optional[str]
    upc_date_store_id: Optional[str]

    def dict(self, *args, **kwargs):
        return {
            "name": self.name,
            "upc": self.upc,
            "price": self.price,
            "basePrice": self.basePrice,
            "pricePer": self.pricePer,
            "averageWeight": self.averageWeight,
            "unitQuantity": self.unitQuantity,
            "departmentName": self.departmentName,
            "salesRank": self.salesRank,
            "unitOfMeasure": self.unitOfMeasure,
            "channelInventory": self.channelInventory,
            "inventoryAvailable": self.inventoryAvailable,
            "promoDescription": self.promoDescription,
            "storeId": self.storeId,
            "date": self.date,
            "area": self.area,
            "upc_date_store_id": self.upc_date_store_id
        }

    def to_db_model(self):
        return SafewayItemDBModel(id=f"{self.upc}_{self.storeId}_{self.date}", name=self.name, upc=self.upc,
                                  date=self.date, storeId=self.storeId, price=self.price, basePrice=self.basePrice,
                                  pricePer=self.pricePer, averageWeight=self.averageWeight,
                                  unitQuantity=self.unitQuantity, departmentName=self.departmentName,
                                  salesRank=self.salesRank, unitOfMeasure=self.unitOfMeasure,
                                  channelInventory=self.channelInventory, inventoryAvailable=self.inventoryAvailable,
                                  promoDescription=self.promoDescription, area=self.area)


Base = declarative_base()


class SafewayItemDBModel(Base):
    __tablename__ = "safeway_item"
    id = Column(String, primary_key=True)
    upc = Column(String, index=True)
    date = Column(TIMESTAMP, index=True)
    storeId = Column(String, index=True)
    name = Column(String)
    price = Column(FLOAT)
    basePrice = Column(FLOAT)
    pricePer = Column(FLOAT)
    averageWeight = Column(String)
    unitQuantity = Column(String)
    departmentName = Column(String)
    salesRank = Column(String)
    unitOfMeasure = Column(String)
    channelInventory = Column(JSON)
    inventoryAvailable = Column(String)
    promoDescription = Column(String)
    area = Column(String)
    storeType = Column(String)

    def to_safeway_object(self):
        return SafewayItem(name=self.name, upc=self.upc, price=self.price, basePrice=self.basePrice,
                           pricePer=self.pricePer, averageWeight=self.averageWeight, unitQuantity=self.unitQuantity,
                           departmentName=self.departmentName, salesRank=self.salesRank,
                           unitOfMeasure=self.unitOfMeasure, channelInventory=self.channelInventory,
                           inventoryAvailable=self.inventoryAvailable, promoDescription=self.promoDescription,
                           storeId=self.storeId, date=self.date, area=self.area, storeType=self.storeType)

    def to_csv(self, fields: list[str]):
        csv_list = []
        object_dict = self.to_safeway_object().dict()
        for field in fields:
            if field in object_dict:
                csv_list.append(object_dict[field])
        return csv_list