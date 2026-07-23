from model.fire import (
    Fire,
    FireMember
)
from repository.base import crud


class FireRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Fire)


class FireMemberRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(FireMember)
