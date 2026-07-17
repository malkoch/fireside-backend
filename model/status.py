import datetime
import enum

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class EStatus(enum.Enum):
    Sent = enum.auto()
    Delivered = enum.auto()
    Read = enum.auto()
    Failed = enum.auto()
    Pending = enum.auto()


class Status(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    user_id: int | None = Field(sa_type=BIGINT)
    time: datetime.datetime = Field(default_factory=datetime.datetime.now)
