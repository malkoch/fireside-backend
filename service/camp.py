import json

from aiokafka import AIOKafkaConsumer
from redis import asyncio as redis


async def run():
    consumer = AIOKafkaConsumer(
        'camp.created', 'camp.user.joined',
        bootstrap_servers='localhost:9092', group_id='1', auto_offset_reset='earliest'
    )
    redis_client = redis.Redis(host='localhost', port=6379)

    await consumer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            print(f'CAMP {message=} {message.topic=} {message.value=}')

            topic = message.topic
            value = message.value.decode('utf-8') if message.value else ''

            if topic == 'camp.created':
                ...
            elif topic == 'camp.user.joined':
                d = json.loads(value)
                camp = d['camp']
                user = d['user']

                await redis_client.sadd(f'camp:{camp}:users', user)
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()
