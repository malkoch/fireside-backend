from typing import Annotated

import jwt
from fastapi import HTTPException
from fastapi.params import Depends

from api.auth import get_token
from core import secret


async def get_roles(token: Annotated[str, Depends(get_token)]):
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['roles']


def require_role(role: str):
    async def checker(roles=Depends(get_roles)):
        if role not in roles:
            raise HTTPException(status_code=403, detail="Do not have required role")

        return roles

    return checker
