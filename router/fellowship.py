import json
from typing import Annotated

import confluent_kafka
from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import SessionDep
from model.fellowship import (
    Fellowship,
    FellowshipMember
)


router = APIRouter(prefix="/fellowship")

producer = confluent_kafka.Producer(
    {
        'bootstrap.servers': 'localhost:9092'
    }
)


@router.post("/create")
def create(fellowship: Fellowship, session: SessionDep) -> Fellowship:
    session.add(fellowship)
    session.commit()
    session.refresh(fellowship)

    producer.produce('fellowship.created', json.dumps({'name': fellowship.name}))

    return fellowship


@router.post("/join")
def join(fellowship_member: FellowshipMember, session: SessionDep) -> FellowshipMember:
    session.add(fellowship_member)
    session.commit()
    session.refresh(fellowship_member)

    producer.produce('fellowship.joined', json.dumps({'fellowship': fellowship_member.fellowship_id, 'user': fellowship_member.user_id}))

    return fellowship_member


@router.get("/list")
def read(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Fellowship]:
    objects = session.exec(select(Fellowship).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{name}")
def delete(name: str, session: SessionDep):
    fellowship = session.exec(select(Fellowship).where(Fellowship.name == name)).first()
    if not fellowship:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(fellowship)
    session.commit()
    return {"ok": True}
