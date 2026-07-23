import datetime
import enum

from sqlalchemy import (
    BIGINT,
    Index
)
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class FireType(enum.Enum):
    Text = enum.auto()
    Voice = enum.auto()


class Fire(SQLModel, table=True):
    __tablename__ = 'fire'

    __table_args__ = (
        Index('unique_fire_name_index', 'camp_id', 'name', unique=True),
    )

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    camp_id: int = Field(index=True, sa_type=BIGINT)
    name: str = Field()
    type: int = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class FireMember(SQLModel, table=True):
    __tablename__ = 'fire_member'

    __table_args__ = (
        Index('unique_fire_member_index', 'fire_id', 'user_id', unique=True),
    )

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    fire_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    joined_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    left_at: datetime.datetime | None = Field(default=None)
