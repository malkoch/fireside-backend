import json
from contextlib import asynccontextmanager
from typing import Annotated

import jwt
from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from sqlmodel import select

from core import secret
from core.session import PGSessionDep
from model.fire import (
    Fire,
    FireMember
)


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/fire", lifespan=lifespan)
security = HTTPBearer()


@router.post("/create")
async def create(
    session: PGSessionDep,
    camp_id: int = Body(...),
    name: str = Body(...),
    type: int = Body(...)
) -> Fire:
    fire = Fire(camp_id=camp_id, name=name, type=type)

    session.add(fire)
    session.commit()
    session.refresh(fire)

    await producer.send('fire.created', json.dumps({'name': fire.name}).encode('utf-8'))

    return fire


@router.post("/join")
async def join(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep,
    fire_id: int = Body(...),
    dummy: int = Body(0)
):
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    fire_member = FireMember(fire_id=fire_id, user_id=payload['user'])

    session.add(fire_member)
    session.commit()
    session.refresh(fire_member)

    await producer.send('fire.user.joined', json.dumps({'fire': fire_member.fire_id, 'user': fire_member.user_id}).encode('utf-8'))

    return fire_member


@router.get("/list")
async def read(
    session: PGSessionDep,
    camp_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Fire]:
    objects = session.exec(select(Fire).where(Fire.camp_id == camp_id).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{name}")
async def delete(
    session: PGSessionDep,
    name: str
):
    campfire = session.exec(select(Fire).where(Fire.name == name)).first()
    if not campfire:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(campfire)
    session.commit()
    return {"ok": True}
