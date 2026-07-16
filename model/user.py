from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class User(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    username: str = Field(index=True, unique=True)
    password: str = Field()


class UserRefreshToken(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    refresh_token: str = Field()
