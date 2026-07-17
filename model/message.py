import datetime

from sqlmodel import (
    BIGINT,
    Field,
    SQLModel
)

from core.snowflake import generator


class Message(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    fire_id: int = Field(sa_type=BIGINT)
    body: str = Field()
    datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)


class MessageDelivery(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    message_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)


class MessageReaction(SQLModel, table=True):
    id: int | None = Field(default_factory=generator(1), primary_key=True, sa_type=BIGINT)
    message_id: int = Field(sa_type=BIGINT)
    user_id: int = Field(sa_type=BIGINT)
    reaction: str = Field()
    datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
