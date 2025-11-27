from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

database_url = os.environ.get("DATABASE_URL")

engine = create_engine(database_url)

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)()

Base = declarative_base()