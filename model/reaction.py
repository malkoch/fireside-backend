import datetime

from sqlalchemy import BIGINT
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class Reaction(SQLModel, table=True):
    __tablename__ = 'reaction'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    reaction: str = Field()
    time: datetime.datetime = Field(default_factory=datetime.datetime.now)
