from fastapi import FastAPI
from routers import users
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    users.users_routers,   
    prefix="/api/v1/users",
)