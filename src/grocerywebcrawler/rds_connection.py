import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


def get_postgres_session():
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session


def get_normal_session():
    engine = get_engine()
    with Session(engine) as session:
        return session


def get_Session_Local() -> Session:
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session


def get_engine():
    load_dotenv()
    AWS_RDS_PATH = os.getenv('AWS_RDS_PATH')
    AWS_RDS_DATABASE_NAME = os.getenv('AWS_RDS_DATABASE_NAME')
    AWS_RDS_PASSWORD =  os.getenv('AWS_RDS_PASSWORD')
    engine = create_engine(
        f"postgresql://postgres:{AWS_RDS_PASSWORD}@{AWS_RDS_PATH}:8886/{AWS_RDS_DATABASE_NAME}",
        pool_size=20, pool_pre_ping=True, pool_recycle=600, max_overflow=0)
    return engine
