import base64
from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from core import call


router = APIRouter(prefix="/image")


@router.get('/{owner_id}')
async def detail(owner_id: int):
    image = await call.get(f'http://127.0.0.1:5000/image/{owner_id}', {})

    return StreamingResponse(
        BytesIO(base64.b64decode(image['content'].replace('data:image/png;base64,', '').encode('utf-8'))),
        media_type='image/png'
    )
