from model.user import (
    User,
    UserRefreshToken
)
from repository.base import crud


class UserRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(User)


class UserRefreshTokenRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(UserRefreshToken)
