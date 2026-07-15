import json

import confluent_kafka
from fastapi import APIRouter

from core.session import PGSessionDep
from model.message import Message


router = APIRouter(prefix="/message")
producer = confluent_kafka.Producer(
    {
        'bootstrap.servers': 'localhost:9092'
    }
)


@router.post("/create")
def create(message: Message, session: PGSessionDep) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)

    producer.produce('message.created', json.dumps({'campfire': message.campfire_id, 'user': message.user_id, 'body': message.body}))

    return message
