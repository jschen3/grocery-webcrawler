from typing import Optional
from sqlalchemy import Column, String, Integer, Boolean
from pydantic.main import BaseModel
from sqlalchemy.orm import declarative_base


class Store(BaseModel):
    storeId: Optional[str]
    location: Optional[str]
    storeType: Optional[str]
    region: Optional[str]
    description: Optional[str]
    webcrawl:Optional[bool]

    def dict(self, *args, **kwargs):
        return {
            "storeId": self.storeId,
            "location": self.location,
            "storeType": self.storeType,
            "region": self.region,
            "description": self.description
        }

    def to_db_model(self):
        return StoreDbModel(storeId=self.storeId, location=self.location, storeType=self.storeType, region=self.region,
                            description=self.description)


Base = declarative_base()


class StoreDbModel(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    storeId = Column(String, index=True)
    location = Column(String, index=True)
    storeType = Column(String, index=True)
    region = Column(String, index=True)
    description = Column(String)
    webcrawl = Column(Boolean)

    def __init__(self, storeId, location, storeType, region, description):
        self.storeId = storeId
        self.location = location
        self.storeType = storeType
        self.region = region
        self.description = description

    def to_store_object(self):
        return Store(storeId=self.storeId, location=self.location, region=self.region, description=self.description)
