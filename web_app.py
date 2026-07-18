from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from starlette.middleware.sessions import SessionMiddleware

from web.router import (
    camp,
    fire,
    home,
    message,
    proxy
)


def create_db_and_tables():
    from core.session import postgresql_engine

    SQLModel.metadata.create_all(postgresql_engine)


app = FastAPI()
app.include_router(camp.router)
app.include_router(fire.router)
app.include_router(home.router)
app.include_router(message.router)
app.include_router(proxy.router)

app.mount("/web/static", StaticFiles(directory="web/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/")
async def index():
    return RedirectResponse("/home/index")
