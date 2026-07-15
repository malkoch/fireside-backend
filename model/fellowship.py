from sqlmodel import (
    Field,
    SQLModel
)


class Fellowship(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    creator_id: int = Field()


class FellowshipMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fellowship_id: int = Field()
    user_id: int = Field()
