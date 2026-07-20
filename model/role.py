import enum

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class ERoleType(enum.Enum):
    Account = enum.auto()
    Camp = enum.auto()
    Fire = enum.auto()


class Role(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    type: int = Field()
    name: str = Field()


class MemberRole(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    role: int = Field(sa_type=BIGINT)
