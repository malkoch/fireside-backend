from fastapi import (
    APIRouter,
    Request
)
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from core import call


router = APIRouter(prefix="/message")
templates = Jinja2Templates(directory="web/templates")


@router.post('/send')
async def send(request: Request):
    body = await request.json()
    message = body.get('message')
    fire_id = body.get('fire_id')

    token = request.cookies.get('access') or ''

    response = await call.post('http://127.0.0.1:5000/message/create', {'fire_id': fire_id, 'body': message}, token)

    return JSONResponse(
        {
            'success': True
        }
    )
