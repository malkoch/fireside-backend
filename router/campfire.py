import json
from contextlib import asynccontextmanager
from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import PGSessionDep
from model.campfire import Campfire


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/campfire", lifespan=lifespan)


@router.post("/create")
async def create(campfire: Campfire, session: PGSessionDep) -> Campfire:
    session.add(campfire)
    session.commit()
    session.refresh(campfire)

    await producer.send('campfire.created', json.dumps({'name': campfire.name}).encode('utf-8'))

    return campfire


@router.post("/join")
async def join(campfire_id: int, user_id: int):
    await producer.send('campfire.user.joined', json.dumps({'campfire': campfire_id, 'user': user_id}).encode('utf-8'))

    return {'ok': True}


@router.get("/list")
async def read(
    fellowship_id: int,
    session: PGSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Campfire]:
    objects = session.exec(select(Campfire).where(Campfire.fellowship_id == fellowship_id).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{name}")
async def delete(name: str, session: PGSessionDep):
    campfire = session.exec(select(Campfire).where(Campfire.name == name)).first()
    if not campfire:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(campfire)
    session.commit()
    return {"ok": True}
