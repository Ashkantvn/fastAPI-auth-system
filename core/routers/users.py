from utils.jwt_manager import create_access_token
from utils.password_manager import verify_password, hash_password
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from models.db.user_model import User
from sqlalchemy.orm import Session

users_routers = APIRouter()

@users_routers.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(username: str, password: str, db: Session= Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_access_token = create_access_token(user_id=new_user.id)
    return {"access_token": new_access_token, "token_type": "bearer"}
    