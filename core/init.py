from sqlmodel import (
    SQLModel,
    select
)

from core.session import get_pg


def create_db_and_tables():
    from core.session import postgresql_engine
    from model.role import (
        Role,
        ERoleType
    )

    SQLModel.metadata.create_all(postgresql_engine)

    with get_pg() as session:
        if not session.exec(select(Role).where(Role.type == ERoleType.App.value)).first():
            session.add(Role(type=ERoleType.App.value, name='user'))
        if not session.exec(select(Role).where(Role.type == ERoleType.App.value)).first():
            session.add(Role(type=ERoleType.App.value, name='admin'))

        if not session.exec(select(Role).where(Role.type == ERoleType.Camp.value)).first():
            session.add(Role(type=ERoleType.Camp.value, name='user'))
        if not session.exec(select(Role).where(Role.type == ERoleType.Camp.value)).first():
            session.add(Role(type=ERoleType.Camp.value, name='admin'))

        if not session.exec(select(Role).where(Role.type == ERoleType.Fire.value)).first():
            session.add(Role(type=ERoleType.Fire.value, name='user'))
        if not session.exec(select(Role).where(Role.type == ERoleType.Fire.value)).first():
            session.add(Role(type=ERoleType.Fire.value, name='admin'))

        session.commit()
