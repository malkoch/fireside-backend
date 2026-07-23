import datetime

from pydantic import BaseModel
from sqlalchemy import (
    BIGINT,
    Index
)
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class Camp(SQLModel, table=True):
    __tablename__ = 'camp'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    name: str = Field(index=True, unique=True)
    creator_id: int = Field(sa_type=BIGINT)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class CampMember(SQLModel, table=True):
    __tablename__ = 'camp_member'

    __table_args__ = (
        Index('unique_camp_member_index', 'camp_id', 'user_id', unique=True),
    )

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    camp_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    joined_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    left_at: datetime.datetime | None = Field(default=None)


class UserCamp(BaseModel):
    id: int
    name: str
    users: list[int]
    icon: str | None
