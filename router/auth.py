import datetime
import hashlib

import jwt
from fastapi import (
    APIRouter,
    HTTPException
)
from sqlmodel import select

from core.secret import JWT_SECRET_KEY
from core.session import PGSessionDep
from model.user import (
    User,
    UserRefreshToken
)


router = APIRouter(prefix="/auth")


@router.post("/authenticate")
async def authenticate(user: User, session: PGSessionDep) -> dict:
    username = user.username
    password = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if db_user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access = jwt.encode(
        {
            'user': db_user.id,
            'sub': username,
            'role': 'user',
            'type': 'access',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    ref = jwt.encode(
        {
            'user': db_user.id,
            'sub': username,
            'role': 'user',
            'type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    refresh_token: UserRefreshToken = UserRefreshToken(user_id=db_user.id, refresh_token=ref)

    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)

    return {
        'access': access,
        'refresh': ref
    }


@router.post("/refresh")
async def refresh(user: User, session: PGSessionDep) -> dict:
    return {
        'access': '',
        'refresh': ''
    }
