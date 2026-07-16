import asyncio
import json

from aiokafka import AIOKafkaConsumer
from redis import asyncio as redis


async def run():
    consumer = AIOKafkaConsumer(
        'message.created',
        bootstrap_servers='localhost:9092', group_id='1', auto_offset_reset='earliest'
    )
    redis_client = redis.Redis(host='localhost', port=6379)

    await consumer.start()

    try:
        async for message in consumer:
            if message is None:
                continue

            print(f'{message=} {message.topic=} {message.value=}')

            topic = message.topic
            value = message.value.decode('utf-8') if message.value else ''

            print(f'{topic}: {value}')

            if topic == 'message.created':
                d = json.loads(value)
                campfire = d['campfire']
                user = d['user']
                body = d['body']

                members = await redis_client.smembers(f'campfire:{campfire}:users')
                members = [member.decode('utf-8') for member in members]
                print(members)
                for member in members:
                    gateway = (await redis_client.get(f'user:{member}:gateway')).decode('utf-8')
                    await redis_client.publish(f'gateway:{gateway}', json.dumps({'campfire': campfire, 'user': user, 'body': body}))
    except KeyboardInterrupt:
        pass
    finally:
        await consumer.stop()


asyncio.run(run())
