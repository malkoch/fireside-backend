from fastapi import (
    APIRouter,
    Request
)

from core import call
from web.core.templates import templates


router = APIRouter(prefix="/fire")


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    fire_id = params.get('fire_id')

    token = request.cookies.get('access') or ''

    messages = await call.get(f'http://127.0.0.1:5000/message/list?fire_id={fire_id}', {}, token)

    return templates.TemplateResponse(request, "fire/detail.html", {'fire_id': fire_id, 'messages': messages})
