import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.BigInteger, primary_key=True)
    login = sa.Column(sa.String(32), unique=True, nullable=False)
    created_at = sa.Column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    password = sa.Column(sa.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<User: id={self.id}, login={self.login}>"


class Logger(Base):
    __tablename__ = "auth_logger"

    id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"), nullable=False)
    token = sa.Column(sa.String(255), nullable=True)
