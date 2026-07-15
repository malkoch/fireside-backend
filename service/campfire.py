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
    consumer.subscribe(['campfire.created', 'campfire.user.joined'])
    while True:
        message = consumer.poll(timeout=1.)
        if message is None:
            continue

        topic = message.topic()
        value = message.value().decode('utf-8') if message.value() else None

        if topic == 'campfire.created':
            ...
        elif topic == 'campfire.user.joined':
            d = json.loads(value)
            campfire = d['campfire']
            user = d['user']

            redis_client.sadd(f'campfire:{campfire}:users', user)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
