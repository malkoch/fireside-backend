from typing import Annotated

import jwt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from core import secret


security = HTTPBearer()


async def get_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = credentials.credentials
    return token


async def get_user(token: Annotated[str, Depends(get_token)]):
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['user']


async def get_roles(token: Annotated[str, Depends(get_token)]):
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['roles']


def require_role(role: str):
    async def checker(roles=Depends(get_roles)):
        if role not in roles:
            raise HTTPException(status_code=403, detail="Do not have required role")

        return roles

    return checker


async def get_permissions(token: Annotated[str, Depends(get_token)]):
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['permissions']


def require_permission(permission: str):
    async def checker(permissions=Depends(get_permissions)):
        if permission not in permissions:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return permissions

    return checker
