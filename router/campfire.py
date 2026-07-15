from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import SessionDep
from model.campfire import Campfire


router = APIRouter(prefix="/campfire")


@router.post("/create")
def create(campfire: Campfire, session: SessionDep) -> str:
    session.add(campfire)
    session.commit()
    session.refresh(campfire)
    return campfire


@router.get("/list")
def read(
    fellowship_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Campfire]:
    objects = session.exec(select(Campfire).where(Campfire.fellowship_id == fellowship_id).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{campfire_id}")
def delete(campfire_id: int, session: SessionDep):
    campfire = session.get(Campfire, campfire_id)
    if not campfire:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(campfire)
    session.commit()
    return {"ok": True}
