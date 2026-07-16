import json
from contextlib import asynccontextmanager
from typing import Annotated

import jwt
from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
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
from model.fellowship import (
    Fellowship,
    FellowshipMember
)


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/fellowship", lifespan=lifespan)
security = HTTPBearer()


@router.post("/create")
async def create(fellowship: Fellowship, session: PGSessionDep) -> Fellowship:
    session.add(fellowship)
    session.commit()
    session.refresh(fellowship)

    await producer.send('fellowship.created', json.dumps({'name': fellowship.name}).encode('utf-8'))

    return fellowship


@router.post("/join")
async def join(fellowship_member: FellowshipMember, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: PGSessionDep) -> FellowshipMember:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    fellowship_member.user_id = payload['user']

    session.add(fellowship_member)
    session.commit()
    session.refresh(fellowship_member)

    await producer.send('fellowship.user.joined', json.dumps({'fellowship': fellowship_member.fellowship_id, 'user': fellowship_member.user_id}).encode('utf-8'))

    return fellowship_member


@router.get("/list")
async def read(
    session: PGSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Fellowship]:
    objects = session.exec(select(Fellowship).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{name}")
async def delete(name: str, session: PGSessionDep):
    fellowship = session.exec(select(Fellowship).where(Fellowship.name == name)).first()
    if not fellowship:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(fellowship)
    session.commit()
    return {"ok": True}
