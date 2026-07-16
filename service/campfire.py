import asyncio
import json

from aiokafka import AIOKafkaConsumer
from redis import asyncio as redis


async def run():
    consumer = AIOKafkaConsumer(
        'campfire.created', 'campfire.user.joined',
        bootstrap_servers='localhost:9092', group_id='1', auto_offset_reset='earliest'
    )
    redis_client = redis.Redis(host='localhost', port=6379)

    await consumer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            topic = message.topic()
            value = message.value().decode('utf-8') if message.value() else ''

            print(f'{topic}: {value}')

            if topic == 'campfire.created':
                ...
            elif topic == 'campfire.user.joined':
                d = json.loads(value)
                campfire = d['campfire']
                user = d['user']

                await redis_client.sadd(f'campfire:{campfire}:users', user)
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()


