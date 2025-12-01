from utils.exceptions import UnAuhthorizedException
from utils.jwt_manager import create_access_token, verify_access_token
from utils.password_manager import verify_password, hash_password
from fastapi import APIRouter, HTTPException, status, Depends, Header
from database import get_db
from models.db.user_model import User
from sqlalchemy.orm import Session
from models.base.base_model import BaseUserModel

users_routers = APIRouter()

# Router for user-related endpoints (signup, login, profile, logout, delete)

@users_routers.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: BaseUserModel, db: Session= Depends(get_db)):
    """Register a new user.

    - Reject if username already exists.
    - Hash the provided password and create the user record.
    - Return a freshly created access token on success.
    """
    db_user = db.query(User).filter(User.username == request.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = hash_password(request.password)
    new_user = User.create_user(
        session=db,
        username=request.username,
        password=hashed_password
    )
    new_access_token = create_access_token(user_id=new_user.id)
    return {
        "data": "User created successfully",
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@users_routers.get("/profile/{username}", status_code=status.HTTP_200_OK)
def profile(username: str, db: Session= Depends(get_db)):
    """Return public profile information for `username`.

    - If the user doesn't exist, return 404.
    """
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return {"profile": {"id": db_user.id, "username": db_user.username}}

@users_routers.post("/login", status_code=status.HTTP_200_OK)
def login(request: BaseUserModel, db: Session= Depends(get_db)):
    """Authenticate a user and return a JWT access token.

    - Verify provided password against stored hash.
    - On success, issue and return an access token.
    - On failure, return 400 with an explanatory message.
    """
    db_user = db.query(User).filter(User.username == request.username).first()
    if db_user:
        valid_password = verify_password(request.password, db_user.password)
        if valid_password:
            access_token = create_access_token(user_id=db_user.id)
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password"
    )

@users_routers.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(authorization: str | None = Header(default=None)):
    """Invalidate the provided access token.

    - Expect `Authorization: Bearer <token>` header.
    - Verify token and (placeholder) add it to a blacklist store.
    - Return 204 on success, 401 on failure.
    """
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
        try:
            verify_access_token(access_token)
            # Add token to blacklist (by redis)
            return
        except:
            raise UnAuhthorizedException()
    raise UnAuhthorizedException()

@users_routers.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete(db: Session= Depends(get_db), authorization: str | None = Header(default=None)):
    """Delete the authenticated user's account.

    - Requires `Authorization: Bearer <token>` header.
    - Verify token to obtain `user_id`, then delete that user record.
    - Return 204 on success, 401 if not authenticated/authorized.
    """
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
        try:
            user_id = verify_access_token(access_token)
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                return
            raise UnAuhthorizedException()
        except:
            raise UnAuhthorizedException()
    raise UnAuhthorizedException()