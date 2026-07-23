from model.reaction import Reaction
from repository.base import crud


class ReactionRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Reaction)
