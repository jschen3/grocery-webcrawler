import json


import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm import sessionmaker


class RDSConnection:
    aws_rds_path: str
    aws_rds_database: str
    aws_rds_password: str

    def __init__(self):
        client = boto3.client('secretsmanager', region_name="us-west-2")
        response = client.get_secret_value(
            SecretId='rds_details'
        )
        database_secrets = json.loads(response['SecretString'])
        self.aws_rds_database=database_secrets["AWS_RDS_DATABASE_NAME"]
        self.aws_rds_path=database_secrets["AWS_RDS_PATH"]
        self.aws_rds_password=database_secrets["AWS_RDS_PASSWORD"]

    def get_postgres_session(self):
        engine = self.get_engine()
        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)
        return session

    def get_normal_session(self):
        engine = self.get_engine()
        with Session(engine) as session:
            return session

    def get_Session_Local(self) -> Session:
        engine = self.get_engine()
        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)
        return session

    def get_engine(self):
        engine = create_engine(
            f"postgresql://postgres:{self.aws_rds_password}@{self.aws_rds_path}:8886/{self.aws_rds_database}",
            pool_size=20, pool_pre_ping=True, pool_recycle=600, max_overflow=0)
        return engine
