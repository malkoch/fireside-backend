import json

import requests


async def post(url: str, data: dict):
    try:
        response = requests.post(
            url,
            json=data,
            headers={}
        )
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def post_authenticated(url: str, data: dict, token: str):
    try:
        response = requests.post(
            url,
            json=data,
            headers={
                'Authorization': f'Bearer {token}',
                'InCase': 'snake',
                'OutCase': 'snake'
            }
        )
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def get(url: str, data: dict):
    try:
        response = requests.get(
            url,
            data=data,
            headers={}
        )
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def get_authenticated(url: str, data: dict, token: str):
    try:
        response = requests.get(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {token}',
                'InCase': 'snake',
                'OutCase': 'snake'
            }
        )
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None
