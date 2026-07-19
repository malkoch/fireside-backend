import json

import requests


async def post(url: str, data: dict, token: str = ''):
    try:
        if token:
            response = requests.post(url, json=data, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'Accept': 'application/json'})
        else:
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def get(url: str, data: dict, token: str = ''):
    try:
        params = '&'.join([f'{key}={value}' for key, value in data.items()])
        if params:
            url += f'?{params}'

        if token:
            response = requests.get(url, data=data, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'Accept': 'application/json'})
        else:
            response = requests.get(url, data=data, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None


async def delete(url: str, token: str = ''):
    try:
        if token:
            response = requests.delete(url, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'Accept': 'application/json'})
        else:
            response = requests.delete(url, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        return json.loads(response.content.decode('utf-8'))
    except Exception as ex:
        print(str(ex))
        return None
