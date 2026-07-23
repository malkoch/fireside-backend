from model.message import Message
from repository.base import crud


class MessageRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Message)
