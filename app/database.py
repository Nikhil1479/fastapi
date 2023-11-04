from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQL_ALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>"
SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:niks1479@localhost/fastapi"

Base = declarative_base()

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)