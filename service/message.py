import json

import confluent_kafka
import redis


consumer = confluent_kafka.Consumer(
    {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 1
    }
)
redis_client = redis.Redis(host='localhost', port=6379)

try:
    consumer.subscribe(['message.created'])
    while True:
        message = consumer.poll(timeout=1.)
        if message is None:
            continue

        topic = message.topic()
        value = message.value().decode('utf-8') if message.value() else None

        if topic == 'message.created':
            d = json.loads(value)
            campfire = d['campfire']
            user = d['user']
            body = d['body']

            members = redis_client.smembers(f'campfire:{campfire}:users')
            members = [member.decode('utf-8') for member in members]
            for member in members:
                gateway = redis_client.get(f'user:{member}:gateway').decode('utf-8')
                redis_client.publish(f'gateway:{gateway}', json.dumps({'campfire': campfire, 'user': user, 'body': body}))
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
