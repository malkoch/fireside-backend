import hashlib
import json
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
    Body
)


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/user", lifespan=lifespan)


@router.post("/register")
async def register(
    username: str = Body(...),
    password: str = Body(...),
    icon: str = Body(...)
):
    await producer.send(
        'user.register',
        json.dumps(
            {
                'username': username,
                'password': hashlib.sha256(password.encode()).hexdigest(),
                'icon': icon
            }
        ).encode('utf-8')
    )
