from model.camp import (
    Camp,
    CampMember
)
from repository.base import crud


class CampRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Camp)


class CampMemberRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(CampMember)
