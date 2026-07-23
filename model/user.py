import datetime

from sqlalchemy import BIGINT
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class User(SQLModel, table=True):
    __tablename__ = 'user'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    username: str = Field(index=True, unique=True)
    password: str = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class UserRefreshToken(SQLModel, table=True):
    __tablename__ = 'user_refresh_token'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    token: str = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
