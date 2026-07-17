from fastapi import (
    APIRouter,
    Request,
    status
)
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from core import call


router = APIRouter(prefix="/fire")
templates = Jinja2Templates(directory="web/templates")


@router.get("/index")
async def index(request: Request):
    response = await call.get('http://127.0.0.1:5000/fire/list', {})

    return templates.TemplateResponse(request, "fire/index.html", {'fires': response})



@router.post('/create')
async def create(request: Request):
    body = await request.json()
    camp_id = body.get('camp_id')
    name = body.get('name')
    type_ = body.get('type')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/fire/create', {'camp_id': camp_id, 'name': name, 'type': type_}, token)

    return JSONResponse({'success': True})

@router.post('/join')
async def join(request: Request):
    body = await request.json()
    fire_id = body.get('fire_id')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/fire/join', {'fire_id': fire_id}, token)

    return RedirectResponse(
        url=f"/fire/detail?fire_id={fire_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    fire_id = params.get('fire_id')

    return templates.TemplateResponse(request, "fire/detail.html", {'fire_id': fire_id})
