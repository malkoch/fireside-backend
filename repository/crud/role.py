from model.role import (
    Role,
    UserRole
)
from repository.base import crud


class RoleRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Role)


class UserRoleRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(UserRole)
