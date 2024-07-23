from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from api.schemas.users import (
    CreateUserSchema,
    UserSchema,
    UpdateUserSchema,
    SessionsSchema,
)

from database.engine import Session
from database.models import User, Logger
from repositories import users as users_repo
from repositories.auth import create_jwt, veryfy_jwt
from repositories.users import get_token_for_delete

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_key = APIKeyHeader(name="Authorization")


def get_current_user(token: str = Security(token_key)):
    decoded_data = veryfy_jwt(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user(decoded_data["user_id"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@router.post("/users")
def create_user(user_data: CreateUserSchema) -> UserSchema:
    password = pwd_context.hash(user_data.password)
    user = User(login=user_data.login, password=password)
    with Session() as session:
        session.add(user)
        session.commit()
    return UserSchema.from_orm(user)


@router.get("/users", response_model=list[UserSchema])
def get_users():
    with Session() as session:
        users = users_repo.get_users(session)
    return users


@router.get("/users/{user_id}", response_model=UserSchema | None)
def get_user(user_id: int):
    with Session() as session:
        user = users_repo.get_user(session, user_id=user_id)
    return user


@router.patch("/users/{user_id}", response_model=UserSchema | None)
def update_user(user_id: int, user_data: UpdateUserSchema) -> User:
    with Session() as session:
        user = users_repo.get_user(session, user_id=user_id)
        user.login = user_data.new_login
        session.commit()
    return user


@router.post("/login")
def authenticate_user(authenticate_data: CreateUserSchema) -> dict:
    with Session() as session:
        user = users_repo.get_user(session, user_login=authenticate_data.login)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    is_password_correct = pwd_context.verify(authenticate_data.password, user.password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    jwt_token, created_at = create_jwt({"user_id": user.id})

    logger_info = Logger(user_id=user.id, token=jwt_token)

    with Session() as session:
        session.add(logger_info)
        session.commit()

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user(token: str = Security(token_key)):
    with Session() as session:
        row = get_token_for_delete(session, token)
        row.token = None
        session.add(row)
        session.commit()
    return {"msg": "Successfully logged out"}


@router.get("/sessions", response_model=list[SessionsSchema])
def get_user_sessions(token: str = Security(token_key)):
    user = get_current_user(token)
    with Session() as session:
        user_sessions = users_repo.get_user_sessions(session, user.id)
    return user_sessions


@router.delete("/sessions")
def close_all_session(token: str = Security(token_key)):
    user = get_current_user(token)
    with Session() as session:
        user_sessions = users_repo.get_user_sessions(session, user.id, token)
        for user_session in user_sessions:
            user_session.token = None
            session.add(user_session)
        session.commit()
    return {"msg": "Successfully logged out"}
