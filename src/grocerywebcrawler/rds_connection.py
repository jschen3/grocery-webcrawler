import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


class RDSConnection:
    __engine = None
    __normal_session = None
    __scoped_session = None

    @staticmethod
    def get_postgres_session():
        if RDSConnection.__scoped_session is None:
            engine = RDSConnection.get_engine()
            session_factory = sessionmaker(bind=engine)
            RDSConnection.__scoped_session = scoped_session(session_factory)
        return RDSConnection.__scoped_session

    @staticmethod
    def get_normal_session():
        if RDSConnection.__normal_session is None:
            engine = RDSConnection.get_engine()
            RDSConnection.__normal_session = Session(engine)
        return RDSConnection.__normal_session

    @staticmethod
    def get_engine():
        if RDSConnection.__engine is None:
            RDSConnection.__engine = create_rds_engine()
        return RDSConnection.__engine

def create_rds_engine():
    load_dotenv()
    AWS_RDS_PATH = os.getenv('AWS_RDS_PATH')
    if AWS_RDS_PATH is None:
        AWS_RDS_PATH = os.environ.get('AWS_RDS_PATH')
    AWS_RDS_PORT = os.getenv('AWS_RDS_PORT')
    if AWS_RDS_PORT is None:
        AWS_RDS_PORT = os.environ.get('AWS_RDS_PORT')
    AWS_RDS_DATABASE_NAME = os.getenv('AWS_RDS_DATABASE_NAME')
    if AWS_RDS_DATABASE_NAME is None:
        AWS_RDS_DATABASE_NAME = os.environ.get('AWS_RDS_DATABASE_NAME')
    AWS_RDS_PASSWORD = os.getenv('AWS_RDS_PASSWORD')
    if AWS_RDS_PASSWORD is None:
        AWS_RDS_PASSWORD = os.getenv('AWS_RDS_PASSWORD')
    engine_url = f"postgresql://postgres:{AWS_RDS_PASSWORD}@{AWS_RDS_PATH}:{AWS_RDS_PORT}/{AWS_RDS_DATABASE_NAME}"
    # print("engine_url:" + engine_url)
    engine = create_engine(engine_url, pool_size=20, pool_pre_ping=True, pool_recycle=600, max_overflow=0)
    return engine
