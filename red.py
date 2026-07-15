import asyncio
import json

import redis

from core.secret import GATEWAY_ID
from core.websocket import manager


redis_client = redis.Redis(host='localhost', port=6379)


async def redis_listener():
    pubsub = redis_client.pubsub()

    pubsub.subscribe(f'gateway:{GATEWAY_ID}')

    print(f'{GATEWAY_ID}')

    for message in pubsub.listen():
        print(message)
        if message['type'] != 'message':
            continue

        print(message)
        packet = json.loads(message['data'])
        await manager.send(packet['user_id'], packet['payload'])


asyncio.run(redis_listener())
