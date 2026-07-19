import json

from fastapi import (
    APIRouter,
    Request
)
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/proxy")


@router.post("/post")
async def post(request: Request):
    from core import call

    body = await request.json()
    controller = body.get('controller', None) or ''
    action = body.get('action', None) or ''
    data = body.get('data', None) or {}

    token = request.cookies.get('access') or ''

    if not controller or not action:
        return JSONResponse(status_code=400, content={'message': 'Controller and action are required'})

    response = await call.post(f'http://127.0.0.1:5000/{controller}/{action}', data, token)

    return JSONResponse(response)


@router.get("/get")
async def get(request: Request):
    from core import call

    params = request.query_params

    controller = params.get('controller', None) or ''
    action = params.get('action', None) or ''
    data = params.get('data', None) or ''
    data = json.loads(data) if data else {}

    token = request.cookies.get('access') or ''

    if not controller or not action:
        return JSONResponse(status_code=400, content={'message': 'Controller and action are required'})

    response = await call.get(f'http://127.0.0.1:5000/{controller}/{action}', data, token)

    return JSONResponse(response)


@router.delete("/")
async def delete(request: Request):
    from core import call

    body = await request.json()
    controller = body.get('controller', None) or ''
    action = body.get('action', None) or ''

    token = request.cookies.get('access') or ''

    if not controller or not action:
        return JSONResponse(status_code=400, content={'message': 'Controller and action are required'})

    response = await call.delete(f'http://127.0.0.1:5000/{controller}/{action}', token)

    return JSONResponse(response)
