import asyncio
import json

import websockets


async def heartbeat(ws):
    while True:
        await ws.send(json.dumps({'op': 'HEARTBEAT'}))

        await asyncio.sleep(5)


async def connect():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjo0Mzc4NDU4ODc5NzQ3NDI4MzUzLCJzdWIiOiJtYWxrb2NoIiwicm9sZSI6InVzZXIiLCJleHAiOjE3ODQxODYyNzh9.ByR6iH-nyDJANwhS__ZUrmEiszpx9yBW18stV_P-Rgc"
    uri = f'ws://localhost:8000/gateway?token={token}'

    async with websockets.connect(uri) as websocket:
        asyncio.create_task(heartbeat(websocket))

        while True:
            response = await websocket.recv()
            print(response)


asyncio.run(connect())
