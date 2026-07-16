from fastapi import (
    APIRouter,
    Request,
    status
)
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from core import call


router = APIRouter(prefix="/campfire")
templates = Jinja2Templates(directory="web/templates")


@router.get("/index")
async def index(request: Request):
    response = await call.get('http://127.0.0.1:5000/campfire/list', {})

    return templates.TemplateResponse(request, "campfire/index.html", {'campfires': response})



@router.post('/create')
async def create(request: Request):
    body = await request.json()
    fellowship_id = body.get('fellowship_id')
    name = body.get('name')
    type_ = body.get('type')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/campfire/create', {'fellowship_id': fellowship_id, 'name': name, 'type': type_}, token)

    return JSONResponse({'success': True})

@router.post('/join')
async def join(request: Request):
    body = await request.json()
    campfire_id = body.get('campfire_id')

    token = request.cookies.get('access') or ''

    response = await call.post_authenticated('http://127.0.0.1:5000/campfire/join', {'campfire_id': campfire_id}, token)

    return RedirectResponse(
        url=f"/campfire/detail?campfire_id={campfire_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/detail')
async def detail(request: Request):
    params = request.query_params
    campfire_id = params.get('campfire_id')

    return templates.TemplateResponse(request, "campfire/detail.html", {'campfire_id': campfire_id})
