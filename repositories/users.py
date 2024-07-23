import datetime
import random
import string

import sqlalchemy as sa
from sqlalchemy.orm import Session

from database.models import User, Logger
from repositories.auth import veryfy_jwt, EXPIRATION_TIME


def get_users(session: Session) -> list[User]:
    return list(
        session.execute(
            sa.select(User).order_by(User.id).limit(10)
        ).scalars().all()
    )


def get_user(session: Session, user_id: int | None = None, user_login: str | None = None) -> User | None:
    if user_id:
        return session.scalar(sa.select(User).where(User.id == user_id))  # noqa
    if user_login:
        return session.scalar(sa.select(User).where(User.login == user_login))  # noqa

def get_token_for_delete(session: Session, token: str):
    return session.scalar(sa.select(Logger).where(Logger.token == token))  # noqa

def get_user_sessions(session: Session, user_id: int, current_token: str | None = None) -> list[User]:
    return list(
        session.scalars(sa.select(Logger).where(Logger.user_id == user_id, Logger.token != current_token)).all()
    )


def get_random_login(length: int = 12) -> str:
    return ''.join(
        [
            random.choice(
                string.ascii_letters
                + string.digits
                + string.punctuation
            )
            for _ in range(length)
        ]
    )
