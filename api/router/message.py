import json
from contextlib import asynccontextmanager
from typing import Annotated

import jwt
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

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
async def create(message: Message, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: PGSessionDep) -> Message:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    message.user_id = payload['user']

    session.add(message)
    session.commit()
    session.refresh(message)

    await producer.send('message.created', json.dumps({'fire': message.fire_id, 'user': message.user_id, 'body': message.body}).encode('utf-8'))

    return message
