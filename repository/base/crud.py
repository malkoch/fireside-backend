from sqlmodel import (
    and_,
    delete,
    insert,
    select,
    update
)


class CRUDRepository:
    def __init__(self, model):
        self._model = model

    def _get_filter(self, query: dict):
        conditions = []
        for key, value in query.items():
            conditions.append(getattr(self._model, key) == value)
        return and_(*conditions)

    async def create(self, session, *objects):
        for obj in objects:
            session.exec(insert(self._model).values(**obj))
        session.commit()

    async def read_one(self, session, query: dict):
        return session.exec(select(self._model).where(self._get_filter(query))).all()

    async def read_list(self, session, query: dict, offset: int, limit: int):
        return session.exec(select(self._model).where(self._get_filter(query)).offset(offset).limit(limit)).all()

    async def read_all(self, session, query: dict):
        return session.exec(select(self._model).where(self._get_filter(query))).all()

    async def update(self, session, query: dict, command):
        session.exec(update(self._model).where(self._get_filter(query)).values(**command))

    async def delete(self, session, query: dict):
        session.exec(delete(self._model).where(self._get_filter(query)))
