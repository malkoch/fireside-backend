from fastapi import (
    APIRouter,
    Request,
    status
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/home")
templates = Jinja2Templates(directory="web/templates")


@router.get("/index")
async def index(request: Request):
    return templates.TemplateResponse(request, "home/index.html")


@router.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "home/login.html")


@router.post("/login")
async def login(request: Request):
    from core import call

    response = await call.post('http://127.0.0.1:5000/auth/authenticate', {'username': 'malkoch', 'password': '1234'})
    access = response['access']
    refresh = response['refresh']

    response = RedirectResponse(
        url="/home/index",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key='access', value=access, httponly=True, secure=False, samesite='lax', max_age=3600)
    response.set_cookie(key='refresh', value=refresh, httponly=True, secure=False, samesite='lax', max_age=3600)

    request.session['user'] = {
        'Name': 'John',
        'Surname': 'Doe'
    }

    return response


@router.get("/logout")
async def logout(request: Request):
    del request.session['user']

    response = RedirectResponse(
        url="/home/index",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie('access')
    response.delete_cookie('refresh')

    return response
