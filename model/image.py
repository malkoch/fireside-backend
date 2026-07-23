from sqlalchemy import BIGINT
from sqlmodel import (
    Field,
    SQLModel
)

from core.snowflake import generator


class Image(SQLModel, table=True):
    __tablename__ = 'image'

    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    owner_id: int = Field(sa_type=BIGINT)
    content: str = Field()
