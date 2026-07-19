import datetime
import json

import redis


def datetime_format(value: datetime.datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    if isinstance(value, str):
        value = datetime.datetime.fromisoformat(value)

    if not value:
        return ''
    return value.strftime(fmt)


def user_name_format(value: int) -> str:
    redis_client = redis.Redis(host='localhost', port=6379)
    user_info = redis_client.get(f'user:{value}:info')
    if not user_info:
        return f'user-{value}'
    return json.loads(user_info.decode('utf-8'))['name']


FILTERS = {
    'datetime': datetime_format,
    'user_name': user_name_format,
}
