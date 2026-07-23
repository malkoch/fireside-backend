from model.status import Status
from repository.base import crud


class StatusRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Status)
