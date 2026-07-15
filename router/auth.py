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
from model.user import User


router = APIRouter(prefix="/auth")


@router.post("/authenticate")
def authenticate(user: User, session: PGSessionDep) -> str:
    username = user.username
    password = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if db_user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    payload = {
        'user': db_user.id,
        'sub': username,
        'role': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    return token
