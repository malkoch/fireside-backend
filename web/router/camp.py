from fastapi import (
    APIRouter,
    Request
)

from core import call
from web.core.templates import templates


router = APIRouter(prefix="/camp")


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    camp_id = params.get('camp_id')

    token = request.cookies.get('access') or ''

    fires = await call.get(f'http://127.0.0.1:5000/fire/list?camp_id={camp_id}', {}, token)

    return templates.TemplateResponse(request, "camp/detail.html", {'fires': fires, 'camp_id': camp_id})
