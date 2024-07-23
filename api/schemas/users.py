from datetime import datetime
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    login: str
    password: str


class UpdateUserSchema(BaseModel):
    new_login: str


class UserSchema(BaseModel):
    id: int
    login: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class SessionsSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
