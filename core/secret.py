import socket
import uuid


JWT_SECRET_KEY = '1234567890'
GATEWAY_ID = f'{socket.gethostname()}-{uuid.uuid4()}'
