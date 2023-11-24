from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user = "root"
password = "root"
mysql = "localhost:3306"
database = "fastapi_example"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{mysql}/{database}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Database = SessionLocal()

Base = declarative_base()

Base.metadata.create_all(bind=engine)