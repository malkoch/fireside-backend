from sqlmodel import (
    Field,
    SQLModel
)


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field()
    campfire_id: int = Field()
    body: str = Field()
