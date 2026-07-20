import enum

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class EPermissionType(enum.Enum):
    Account = enum.auto()
    Camp = enum.auto()
    Fire = enum.auto()


class EPermission(enum.Enum):
    create = enum.auto()
    read = enum.auto()
    update = enum.auto()
    delete = enum.auto()


class Permission(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    type: int = Field()
    permission: int = Field()
