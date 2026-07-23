from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session


postgresql_engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/fireside')


def get_pg():
    return Session(postgresql_engine)


def get_pg_session():
    with get_pg() as session:
        yield session


PGSessionDep = Annotated[Session, Depends(get_pg_session)]
