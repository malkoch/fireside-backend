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

from api.auth import get_user
from core import secret
from core.session import PGSessionDep
from model.camp import (
    Camp,
    CampMember,
    UserCamp
)
from model.image import Image


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
async def create(
    user: Annotated[int, Depends(get_user)],
    name: str = Body(...),
    icon: str = Body(...)
):
    await producer.send(
        'camp.create',
        json.dumps(
            {
                'user': user,
                'name': name,
                'icon': icon
            }
        ).encode('utf-8')
    )


@router.post("/join")
async def join(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep,
    name: str = Body(...),
    dummy: int = Body(0)
) -> CampMember:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    camp = session.exec(select(Camp).where(Camp.name == name)).first()

    camp_member = CampMember(camp_id=camp.id, user_id=payload['user'])

    session.add(camp_member)
    session.commit()
    session.refresh(camp_member)

    await producer.send('camp.user.joined', json.dumps({'camp': camp_member.camp_id, 'user': camp_member.user_id}).encode('utf-8'))

    return camp_member


@router.post("/leave")
async def leave(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep,
    name: str = Body(...),
    dummy: int = Body(0)
) -> CampMember:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    camp = session.exec(select(Camp).where(Camp.name == name)).first()

    camp_member = CampMember(camp_id=camp.id, user_id=payload['user'])

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


@router.get('/user-camps')
async def read_user_camps(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: PGSessionDep
) -> list[UserCamp]:
    token = credentials.credentials
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    camp_members = session.exec(select(CampMember).where(CampMember.user_id == payload['user'])).all()

    objects = []
    for camp_member in camp_members:
        camp = session.exec(select(Camp).where(Camp.id == camp_member.camp_id)).first()
        camp_users = session.exec(select(CampMember).where(CampMember.camp_id == camp.id)).all()
        camp_image = session.exec(select(Image).where(Image.owner_id == camp.id)).first()

        user_camp = UserCamp(
            id=camp.id,
            name=camp.name,
            users=[camp_user.user_id for camp_user in camp_users],
            icon=camp_image.content if camp_image else None
        )
        objects.append(user_camp)
    return objects


@router.delete("/{name}")
async def delete(
    session: PGSessionDep,
    name: str
):
    fellowship = session.exec(select(Camp).where(Camp.name == name)).first()
    if not fellowship:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(fellowship)
    session.commit()
    return {"ok": True}
