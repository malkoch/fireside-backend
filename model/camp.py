from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class Camp(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    name: str = Field(index=True, unique=True)
    creator_id: int = Field(sa_type=BIGINT)


class CampMember(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    camp_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
