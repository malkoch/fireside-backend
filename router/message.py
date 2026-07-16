import json
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter

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


@router.post("/create")
async def create(message: Message, session: PGSessionDep) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)

    await producer.send('message.created', json.dumps({'campfire': message.campfire_id, 'user': message.user_id, 'body': message.body}).encode('utf-8'))

    return message
