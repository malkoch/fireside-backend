import hashlib
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import PGSessionDep
from model.user import User


router = APIRouter(prefix="/user")


@router.post("/create")
def create_user(user: User, session: PGSessionDep) -> User:
    user = User(
        username=user.username,
        password=hashlib.sha256(user.password.encode()).hexdigest()
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/list/")
def read_users(
    session: PGSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}")
def read_user(user_id: int, session: PGSessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: PGSessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
