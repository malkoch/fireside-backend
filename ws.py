import asyncio

import websockets


async def connect():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxLCJzdWIiOiJtYWxrb2NoIiwicm9sZSI6InVzZXIiLCJleHAiOjE3ODQxMzUxMTl9.lxHk9DrcfCTktHOKqgey6cB0etSggfdpgoziMQNVmec"
    uri = f'ws://localhost:8000/gateway?token={token}'

    async with websockets.connect(uri) as websocket:
        await websocket.send('Hello, world!')

        response = await websocket.recv()
        print(response)


asyncio.run(connect())
