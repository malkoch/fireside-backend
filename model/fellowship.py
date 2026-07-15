from sqlmodel import (
    Field,
    SQLModel
)


class Fellowship(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
