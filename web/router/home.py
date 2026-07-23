import base64

from fastapi import (
    APIRouter,
    Request,
    status
)
from fastapi.responses import (
    RedirectResponse
)

from web.core.templates import templates


router = APIRouter(prefix="/home")


@router.get("/index")
async def index(request: Request):
    if request.session and request.session['user']:
        return templates.TemplateResponse(request, "home/index.html")
    else:
        return RedirectResponse(url="/home/login-page", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "home/login.html")


@router.post("/login")
async def login(request: Request):
    from core import call

    form = await request.form()

    username = form.get('username')
    password = form.get('password')

    response = await call.post('http://127.0.0.1:5000/auth/authenticate', {'username': username, 'password': password})
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


@router.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse(request, "home/register.html")


@router.post("/register")
async def register(request: Request):
    from core import call

    form = await request.form()

    icon = base64.b64encode(await form.get('icon').read()).decode('utf-8')
    username = form.get('username')
    password = form.get('password')
    re_password = form.get('repassword')

    if password != re_password:
        return RedirectResponse(
            url='/home/register-page',
            status_code=status.HTTP_303_SEE_OTHER
        )

    response = await call.post('http://127.0.0.1:5000/user/register', {'username': username, 'password': password, 'icon': icon})

    response = RedirectResponse(
        url="/home/index",
        status_code=status.HTTP_303_SEE_OTHER
    )

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
