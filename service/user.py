import json

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer
)
from redis import asyncio as redis

from core.session import get_pg
from core.snowflake import generator
from repository.crud.user import UserRepository


async def run():
    consumer = AIOKafkaConsumer(
        'user.register', 'user.registered',
        'user.login', 'user.loggedin',
        'user.logout', 'user.loggedout',
        bootstrap_servers='localhost:9092', group_id='1'
    )
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')

    redis_client = redis.Redis(host='localhost', port=6379)

    user_repository = UserRepository()

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            print(f'USER {message=} {message.topic=} {message.value=}')

            topic = message.topic
            value = message.value.decode('utf-8') if message.value else ''

            data = json.loads(value)
            if topic == 'user.register':
                user_id = generator(1)()
                username = data['username']
                password = data['password']
                icon = data['icon']

                with get_pg() as sess:
                    await user_repository.create(sess, {'id': user_id, 'username': username, 'password': password})

                await producer.send('user.registered', json.dumps({'user': user_id}).encode('utf-8'))

                if icon:
                    await producer.send('image.create', json.dumps({'owner': user_id, 'icon': icon}).encode('utf-8'))
            elif topic == 'user.registered':
                with get_pg() as sess:
                    user = await user_repository.read_one(sess, {'id': data['user']})
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()
        await producer.stop()
