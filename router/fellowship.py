from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import SessionDep
from model.fellowship import Fellowship


router = APIRouter(prefix="/fellowship")


@router.post("/create")
def create(fellowship: Fellowship, session: SessionDep) -> str:
    session.add(fellowship)
    session.commit()
    session.refresh(fellowship)
    return fellowship


@router.get("/list")
def read(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Fellowship]:
    objects = session.exec(select(Fellowship).offset(offset).limit(limit)).all()
    return objects


@router.delete("/{fellowship_id}")
def delete(fellowship_id: int, session: SessionDep):
    fellowship = session.get(Fellowship, fellowship_id)
    if not fellowship:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(fellowship)
    session.commit()
    return {"ok": True}
