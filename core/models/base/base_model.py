from pydantic import BaseModel

class BaseUserModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True