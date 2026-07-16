from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class Message(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    user_id: int = Field()
    campfire_id: int = Field()
    body: str = Field()
