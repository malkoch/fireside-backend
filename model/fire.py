import enum

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class FireType(enum.Enum):
    Text = enum.auto()
    Voice = enum.auto()


class Fire(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    camp_id: int = Field(index=True, sa_type=BIGINT)
    name: str = Field()
    type: int = Field()


class FireMember(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    fire_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
