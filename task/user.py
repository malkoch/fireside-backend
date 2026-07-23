import json

import redis
from sqlalchemy import create_engine
from sqlmodel import (
    Session,
    select
)

from model.user import User
from task.celery import celery


@celery.task
def sync_data():
    redis_client = redis.Redis(host='localhost', port=6379)
    postgresql_engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/fireside')

    with Session(postgresql_engine) as session:
        users = session.exec(select(User)).all()

        for user in users:
            redis_client.set(
                f'user:{user.id}:info', json.dumps(
                    {
                        'id': user.id,
                        'name': user.username
                    }
                )
            )
