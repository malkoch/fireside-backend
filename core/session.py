from typing import Annotated

from fastapi import Depends
from sqlmodel import (
    Session,
    create_engine
)


postgresql_engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/fireside')


def get_session():
    with Session(postgresql_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
