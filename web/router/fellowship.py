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


router = APIRouter(prefix="/fellowship")
templates = Jinja2Templates(directory="web/templates")


@router.get("/index")
async def index(request: Request):
    response = await call.get('http://127.0.0.1:5000/fellowship/list', {})

    return templates.TemplateResponse(request, "fellowship/index.html", {'fellowships': response})


@router.post('/create')
async def create(request: Request):
    body = await request.json()
    name = body.get('name')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/fellowship/create', {'name': name}, token)

    return JSONResponse({'success': True})


@router.post('/join')
async def join(request: Request):
    body = await request.json()
    fellowship_id = body.get('fellowship_id')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/fellowship/join', {'fellowship_id': fellowship_id}, token)

    return RedirectResponse(
        url=f"/fellowship/detail?fellowship_id={fellowship_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    fellowship_id = params.get('fellowship_id')

    token = request.cookies.get('access') or ''

    campfires = await call.get_authenticated(f'http://127.0.0.1:5000/campfire/list?fellowship_id={fellowship_id}', {}, token)

    return templates.TemplateResponse(request, "fellowship/detail.html", {'campfires': campfires, 'fellowship_id': fellowship_id})
