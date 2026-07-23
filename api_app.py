import asyncio
import datetime
import json

import jwt
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as redis

from api.router import (
    auth,
    camp,
    fire,
    image,
    message,
    user
)
from core import secret
from core.init import create_db_and_tables
from core.secret import GATEWAY_ID
from core.websocket import manager


app = FastAPI()
app.include_router(auth.router)
app.include_router(camp.router)
app.include_router(fire.router)
app.include_router(image.router)
app.include_router(message.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get('/')
async def index():
    return {
        'ok': True
    }


@app.websocket('/gateway')
async def gateway(ws: WebSocket):
    if ws.cookies.get('access', None):
        token = ws.cookies.get('access')
    elif ws.headers.get('Authorization', None):
        token = ws.headers['Authorization'].split('Bearer ')[1]
    elif ws.query_params.get('access', None):
        token = ws.query_params['access']
    else:
        token = ''

    if not token:
        await ws.close()
        return

    payload = jwt.decode(token, key=secret.JWT_SECRET_KEY, algorithms=['HS256'])

    user_id = payload['user']
    await manager.connect(user_id, ws)

    await redis_client.set(f'user:{user_id}:gateway', GATEWAY_ID)

    try:
        while True:
            recv = await ws.receive_text()

            packet = json.loads(recv)
            print(packet)
            if packet['op'] == 'HEARTBEAT':
                await redis_client.set(f'user:{user_id}:heartbeat', datetime.datetime.utcnow().isoformat())
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        await redis_client.delete(f'user:{user_id}:gateway')
