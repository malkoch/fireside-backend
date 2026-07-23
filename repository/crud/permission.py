from model.permission import Permission
from repository.base import crud


class PermissionRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Permission)
