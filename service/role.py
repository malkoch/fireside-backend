import json

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer
)
from redis import asyncio as redis

from core.session import get_pg
from core.snowflake import generator
from repository.crud.camp import (
    CampMemberRepository,
    CampRepository
)
from repository.crud.user import UserRepository


async def run():
    consumer = AIOKafkaConsumer(
        'role.create', 'role.created',
        'role.grant', 'role.granted',
        'role.revoke', 'role.revoked',
        bootstrap_servers='localhost:9092', group_id='1'
    )
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')

    redis_client = redis.Redis(host='localhost', port=6379)

    camp_repository = CampRepository()
    camp_member_repository = CampMemberRepository()
    user_repository = UserRepository()

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            print(f'ROLE {message=} {message.topic=} {message.value=}')

            topic = message.topic
            value = message.value.decode('utf-8') if message.value else ''

            data = json.loads(value)
            if topic == 'camp.create':
                camp_id = generator(1)()
                user = data['user']
                name = data['name']
                icon = data['icon']

                with get_pg() as sess:
                    await camp_repository.create(sess, {'id': camp_id, 'name': name, 'creator_id': user})

                await producer.send('camp.created', json.dumps({'camp': camp_id}).encode('utf-8'))

                if icon:
                    await producer.send('image.create', json.dumps({'owner': camp_id, 'icon': icon}).encode('utf-8'))
            elif topic == 'camp.created':
                with get_pg() as sess:
                    camp = await camp_repository.read_one(sess, {'id': data['camp']})

                await producer.send('camp.user.join', json.dumps({'camp': camp.id, 'user': camp.creator_id}).encode('utf-8'))
                await producer.send('fire.create', json.dumps({'camp': camp.id, 'name': 'camp-log'}).encode('utf-8'))
            elif topic == 'camp.user.join':
                member_id = generator(1)()
                camp = await camp_repository.read_one(sess, {'id': data['camp']})
                user = await user_repository.read_one(sess, {'id': data['user']})

                with get_pg() as sess:
                    await camp_member_repository.create(sess, {'id': member_id, 'camp_id': camp.id, 'user_id': user.id})

                await producer.send('camp.user.joined', json.dumps({'member': member_id}).encode('utf-8'))
            elif topic == 'camp.user.joined':
                member = await camp_member_repository.read_one(sess, {'id': data['member']})

                await redis_client.sadd(f'camp:{camp}:users', member.user_id)

                await producer.send('message.create', json.dumps({'camp': member.camp_id, 'user': member.user_id, 'message': 'Hi I have joined the channel'}).encode('utf-8'))
            elif topic == 'camp.delete':
                ...
            elif topic == 'camp.deleted':
                ...
            elif topic == 'camp.user.leave':
                ...
            elif topic == 'camp.user.left':
                ...
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()
        await producer.stop()
