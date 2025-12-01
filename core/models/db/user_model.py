from sqlalchemy import Column, String, Integer
from database import Base
from sqlalchemy.orm import Session
from utils.password_manager import hash_password

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,  index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    @classmethod
    def create_user(cls, session:Session, username:str, password:str):
        password = hash_password(password)
        new_user = cls(username=username, password=password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user