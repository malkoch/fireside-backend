import datetime
import hashlib

import jwt
from fastapi import (
    APIRouter,
    Body,
    HTTPException
)
from sqlmodel import select

from core import secret
from core.secret import JWT_SECRET_KEY
from core.session import PGSessionDep
from model.permission import (
    EPermission,
    EPermissionType,
    Permission
)
from model.role import (
    ERoleType,
    Role, UserRole
)
from model.user import (
    User,
    UserRefreshToken
)


router = APIRouter(prefix="/auth")


@router.post("/authenticate")
async def authenticate(
    session: PGSessionDep,
    username: str = Body(...),
    password: str = Body(...)
) -> dict:
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if db_user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    permissions = session.exec(select(Permission).where(Permission.owner_id == db_user.id)).all()
    permissions = list(map(lambda x: f'{EPermissionType(x.type).name}.{EPermission(x.permission).name}', permissions))

    roles = session.exec(select(MemberRole).where(MemberRole.owner_id == db_user.id)).all()
    for role in roles:
        role.role_type = session.exec(select(Role).where(Role.id == role.role)).first()
    roles = list(map(lambda x: f'{ERoleType(x.role_type.type).name}.{x.role_type.name}', roles))

    access = jwt.encode(
        {
            'user': db_user.id,
            'roles': roles,
            'permissions': permissions,
            'type': 'access',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    ref = jwt.encode(
        {
            'user': db_user.id,
            'type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    refresh_token: UserRefreshToken = UserRefreshToken(user_id=db_user.id, refresh_token=hashlib.sha256(ref.encode('utf-8')).hexdigest())

    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)

    return {
        'access': access,
        'refresh': ref
    }


@router.post("/refresh")
async def refresh(
    session: PGSessionDep,
    ref: str = Body(...)
) -> dict:
    payload = jwt.decode(ref, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    if payload['type'] not in ('refresh',):
        raise ValueError('this is not a refresh token')

    user_id = payload['user']

    db_token = session.exec(select(UserRefreshToken).where(UserRefreshToken.user_id == user_id)).first()
    if not db_token:
        raise ValueError('refresh token not found')
    if db_token.token != hashlib.sha256(ref.encode('utf-8')).hexdigest():
        raise ValueError('refresh token not found')

    access = jwt.encode(
        {
            'user': user_id,
            'role': 'user',
            'type': 'access',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    ref = jwt.encode(
        {
            'user': user_id,
            'role': 'user',
            'type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }, JWT_SECRET_KEY, algorithm="HS256"
    )

    refresh_token: UserRefreshToken = UserRefreshToken(user_id=user_id, refresh_token=ref)

    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)

    return {
        'access': access,
        'refresh': ref
    }
