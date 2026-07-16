import enum

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class CampfireType(enum.Enum):
    Text = enum.auto()
    Voice = enum.auto()


class Campfire(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    fellowship_id: int = Field(index=True)
    name: str = Field()
    type: int = Field()
