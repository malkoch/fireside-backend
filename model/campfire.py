import enum

from sqlmodel import (
    Field,
    SQLModel
)


class CampfireType(enum.Enum):
    Text = enum.auto()
    Voice = enum.auto()


class Campfire(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fellowship_id: int = Field(index=True)
    name: str = Field()
    type: int = Field()
