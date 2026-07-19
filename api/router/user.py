import hashlib
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query
)
from sqlmodel import select

from core.session import PGSessionDep
from model.image import Image
from model.user import User


router = APIRouter(prefix="/user")


@router.post("/create")
async def create_user(
    session: PGSessionDep,
    username: str = Body(...),
    password: str = Body(...),
    icon: str = Body(...)
) -> User:
    user = User(
        username=username,
        password=hashlib.sha256(password.encode()).hexdigest()
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    if icon:
        image = Image(owner_id=user.id, content=icon)
        session.add(image)
        session.commit()
        session.refresh(image)

    return user


@router.get("/list/")
async def read_users(
    session: PGSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}")
async def read_user(
    session: PGSessionDep,
    user_id: int
) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
    session: PGSessionDep,
    user_id: int
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
