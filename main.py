import asyncio
import datetime
import json

import jwt
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)
from redis import asyncio as redis
from sqlmodel import SQLModel

from core import secret
from core.secret import GATEWAY_ID
from core.websocket import manager
from router import (
    auth,
    campfire,
    fellowship,
    message,
    user
)


def create_db_and_tables():
    from core.session import postgresql_engine

    SQLModel.metadata.create_all(postgresql_engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(campfire.router)
app.include_router(fellowship.router)
app.include_router(message.router)
app.include_router(user.router)

redis_client = redis.Redis(host='localhost', port=6379)


async def redis_listener():
    pubsub = redis_client.pubsub()

    await pubsub.subscribe(f'gateway:{GATEWAY_ID}')

    while True:
        msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if msg is None:
            continue

        if msg['type'] != 'message':
            continue

        packet = json.loads(msg['data'])
        await manager.send(packet['user'], packet)


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

    asyncio.create_task(redis_listener())


@app.websocket('/gateway')
async def gateway(ws: WebSocket):
    token = ws.query_params['token']
    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    user_id = payload['user']
    await manager.connect(user_id, ws)

    await redis_client.set(f'user:{user_id}:gateway', GATEWAY_ID)

    try:
        while True:
            recv = await ws.receive_text()

            packet = json.loads(recv)
            if packet['op'] == 'HEARTBEAT':
                await redis_client.set(f'user:{user_id}:heartbeat', datetime.datetime.utcnow().isoformat())
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        await redis_client.delete(f'user:{user_id}:gateway')
