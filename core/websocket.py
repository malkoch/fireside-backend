from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.connections[user_id] = websocket

    async def disconnect(self, user_id):
        self.connections.pop(user_id)

    async def send(self, user_id, payload):
        websocket = self.connections.get(user_id)
        if websocket is None:
            return

        try:
            await websocket.send_json(payload)
        except Exception:
            self.connections.pop(user_id)


manager = ConnectionManager()
