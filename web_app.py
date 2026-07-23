from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from core.init import create_db_and_tables
from web.router import (
    camp,
    fire,
    home,
    image,
    proxy
)



app = FastAPI()
app.include_router(camp.router)
app.include_router(fire.router)
app.include_router(home.router)
app.include_router(image.router)
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
