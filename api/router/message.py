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
from model.message import Message


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/message", lifespan=lifespan)
security = HTTPBearer()


@router.post("/create")
async def create(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep,
    fire_id: int = Body(...),
    body: str = Body(...)
) -> Message:
    if not body:
        return None

    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    message = Message(fire_id=fire_id, body=body, user_id=payload['user'])

    session.add(message)
    session.commit()
    session.refresh(message)

    await producer.send('message.created', json.dumps({'fire': message.fire_id, 'user': message.user_id, 'body': message.body}).encode('utf-8'))

    return message


@router.get("/list")
async def read(
    session: PGSessionDep,
    fire_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Message]:
    objects = session.exec(select(Message).where(Message.fire_id == fire_id).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{message_id}")
async def create(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep,
    message_id: int
):
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    message = session.exec(select(Message).where(Message.id == message_id)).first()
    if not message:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(message)
    session.commit()
    return {"ok": True}
