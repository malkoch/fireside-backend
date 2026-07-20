from typing import Annotated

import jwt
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
