from fastapi import FastAPI
from sqlmodel import SQLModel

from router import (
    auth,
    campfire,
    fellowship,
    user
)


def create_db_and_tables():
    from core.session import postgresql_engine

    SQLModel.metadata.create_all(postgresql_engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(campfire.router)
app.include_router(fellowship.router)
app.include_router(user.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
