from fastapi import (
    APIRouter,
    Request,
    status
)
from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)
from fastapi.templating import Jinja2Templates

from core import call


router = APIRouter(prefix="/camp")
templates = Jinja2Templates(directory="web/templates")


@router.get("/index")
async def index(request: Request):
    response = await call.get('http://127.0.0.1:5000/camp/list', {})

    return templates.TemplateResponse(request, "camp/index.html", {'camps': response})


@router.post('/create')
async def create(request: Request):
    body = await request.json()
    name = body.get('name')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/camp/create', {'name': name}, token)

    return JSONResponse({'success': True})


@router.post('/join')
async def join(request: Request):
    body = await request.json()
    camp_id = body.get('camp_id')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/camp/join', {'camp_id': camp_id}, token)

    return RedirectResponse(
        url=f"/camp/detail?camp_id={camp_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    camp_id = params.get('camp_id')

    token = request.cookies.get('access') or ''

    fires = await call.get_authenticated(f'http://127.0.0.1:5000/fire/list?camp_id={camp_id}', {}, token)

    return templates.TemplateResponse(request, "camp/detail.html", {'fires': fires, 'camp_id': camp_id})
