import json

import requests


async def post(url: str, data: dict, token: str = ''):
    try:
        if token:
            response = requests.post(url, json=data, headers={'Authorization': f'Bearer {token}'})
        else:
            response = requests.post(url, json=data, headers={})
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def get(url: str, data: dict, token: str = ''):
    try:
        if token:
            response = requests.get(url, data=data, headers={'Authorization': f'Bearer {token}'})
        else:
            response = requests.get(url, data=data, headers={})
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None
