import json
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
    Body,
    HTTPException
)
from fastapi.security import (
    HTTPBearer
)
from sqlmodel import select

from core.session import PGSessionDep
from model.image import Image


producer: AIOKafkaProducer


@asynccontextmanager
async def lifespan(app: APIRouter):
    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    yield

    await producer.stop()


router = APIRouter(prefix="/image", lifespan=lifespan)
security = HTTPBearer()


@router.post("/create")
async def create(
    session: PGSessionDep,
    owner_id: int = Body(...),
    content: str = Body(...)
) -> Image:
    image = Image(owner_id=owner_id, content=content)

    session.add(image)
    session.commit()
    session.refresh(image)

    await producer.send('image.created', json.dumps({'content': image.content}).encode('utf-8'))

    return image


@router.get("/{camp_id}")
async def read(
    session: PGSessionDep,
    camp_id: int
) -> Image:
    image = session.exec(select(Image).where(Image.owner_id == camp_id)).first()
    return image


@router.delete("/{image_id}")
async def delete(
    session: PGSessionDep,
    image_id: str
):
    image = session.exec(select(Image).where(Image.id == image_id)).first()
    if not image:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(image)
    session.commit()
    return {"ok": True}
