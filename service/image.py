import json

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer
)
from redis import asyncio as redis

from core.session import get_pg
from core.snowflake import generator
from repository.crud.image import ImageRepository


async def run():
    consumer = AIOKafkaConsumer(
        'image.create', 'image.created',
        bootstrap_servers='localhost:9092', group_id='1'
    )
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')

    redis_client = redis.Redis(host='localhost', port=6379)

    image_repository = ImageRepository()

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            print(f'IMAGE {message=} {message.topic=} {message.value=}')

            topic = message.topic
            value = message.value.decode('utf-8') if message.value else ''

            data = json.loads(value)
            if topic == 'image.create':
                image_id = generator(1)()
                owner = data['owner']
                content = data['content']

                with get_pg() as sess:
                    await image_repository.create(sess, {'id': image_id, 'owner_id': owner, 'content': content})

                await producer.send('image.created', json.dumps({'image': image_id}).encode('utf-8'))
            elif topic == 'image.created':
                with get_pg() as sess:
                    image = await image_repository.read_one(sess, {'id': data['image']})

                await redis_client.set(f'image:{image.id}:content', image.content)
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()
        await producer.stop()
