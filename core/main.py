from fastapi import FastAPI
from routers import users
from database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: drop database tables
    Base.metadata.drop_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(
    users.users_routers,
    prefix="/api/v1/users",
)