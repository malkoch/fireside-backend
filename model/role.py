import enum

from sqlalchemy import BIGINT
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class ERoleType(enum.Enum):
    App = enum.auto()
    Camp = enum.auto()
    Fire = enum.auto()


class Role(SQLModel, table=True):
    __tablename__ = 'role'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    type: int | None = Field()
    name: str = Field()


class UserRole(SQLModel, table=True):
    __tablename__ = 'user_role'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    role: int = Field(sa_type=BIGINT)
