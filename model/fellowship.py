from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class Fellowship(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    name: str = Field(index=True, unique=True)
    creator_id: int = Field(sa_type=BIGINT)


class FellowshipMember(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    fellowship_id: int = Field(sa_type=BIGINT)
    user_id: int = Field()
