from sqlalchemy import Column, String, Integer
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,  index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)