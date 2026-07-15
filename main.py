import asyncio
import json
import socket
import uuid

import jwt
import redis
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)
from sqlmodel import SQLModel

from core import secret
from core.websocket import manager
from router import (
    auth,
    campfire,
    fellowship,
    user
)


def create_db_and_tables():
    from core.session import postgresql_engine

    SQLModel.metadata.create_all(postgresql_engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(campfire.router)
app.include_router(fellowship.router)
app.include_router(user.router)

GATEWAY_ID = f'{socket.gethostname()}-{uuid.uuid4()}'

redis_client = redis.Redis(host='localhost', port=6379)


async def redis_listener():
    pubsub = redis_client.pubsub()

    pubsub.subscribe(f'gateway:{GATEWAY_ID}')

    async for message in pubsub.listen():
        if message['type'] != 'message':
            continue

        packet = json.loads(message['data'])
        await manager.send(packet['user_id'], packet['payload'])


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

    asyncio.create_task(redis_listener())


@app.websocket('/gateway')
async def gateway(ws: WebSocket):
    # validate token
    token = ws.query_params['token']
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    user_id = payload['user']
    await manager.connect(user_id, ws)

    redis_client.set(f'user:{user_id}:gateway', GATEWAY_ID)

    try:
        while True:
            recv = await ws.receive_text()
            print(f'user:{user_id}:recv', recv)
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        redis_client.delete(f'user:{user_id}:gateway')
