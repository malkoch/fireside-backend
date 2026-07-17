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
from model.camp import (
    Camp,
    CampMember
)


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/camp", lifespan=lifespan)
security = HTTPBearer()


@router.post("/create")
async def create(camp: Camp, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: PGSessionDep) -> Camp:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    camp.creator_id = payload['user']

    session.add(camp)
    session.commit()
    session.refresh(camp)

    await producer.send('camp.created', json.dumps({'name': camp.name}).encode('utf-8'))

    return camp


@router.post("/join")
async def join(camp_member: CampMember, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: PGSessionDep) -> CampMember:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    camp_member.user_id = payload['user']

    session.add(camp_member)
    session.commit()
    session.refresh(camp_member)

    await producer.send('camp.user.joined', json.dumps({'camp': camp_member.camp_id, 'user': camp_member.user_id}).encode('utf-8'))

    return camp_member


@router.get("/list")
async def read(
    session: PGSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Camp]:
    objects = session.exec(select(Camp).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{name}")
async def delete(name: str, session: PGSessionDep):
    fellowship = session.exec(select(Camp).where(Camp.name == name)).first()
    if not fellowship:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(fellowship)
    session.commit()
    return {"ok": True}
