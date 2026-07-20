from typing import Annotated

import jwt
from fastapi import HTTPException
from fastapi.params import Depends

from api.auth import get_token
from core import secret


async def get_permissions(token: Annotated[str, Depends(get_token)]):
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['permissions']


def require_permission(permission: str):
    async def checker(permissions=Depends(get_permissions)):
        if permission not in permissions:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return permissions

    return checker
