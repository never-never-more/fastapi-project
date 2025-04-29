from fastapi import FastAPI, Path, Query, Body, Request, Form, status
from fastapi.responses import  HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Cookie
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime

class LoginForm(BaseModel):
    username: str
    password: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)                                  #   Request — это класс из модуля fastapi,
async def get_home(request: Request):                                       #   который предоставляет доступ к:
    username = request.cookies.get("username")                              #   headers, cookies, form(), body() и т.д.
    return templates.TemplateResponse("home.html",
      {"request":request, "username": username, "date":datetime.now()})


@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("about.html",
      {"request":request, "username": username, "date":datetime.now()})

@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("contact.html",
      {"request":request, "username": username, "date":datetime.now()})

@app.get("/login", response_class=HTMLResponse)                             #   Получить HTML страницу логин
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")                                                         #   Создана интерактивная логин форма 
async def post_login(   requset: Request,
                        username: str = Form(...),
                        password: str = Form(...)   ):
    
    form_data = LoginForm(  username=username,
                            password=password   )
    
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=username)
    return response 

@app.get("/logout")
async def get_logout():
    response = RedirectResponse("/")
    response.delete_cookie("username")
    return response

@app.get("/registr", response_class=HTMLResponse)
async def get_registr(request: Request):
    return templates.TemplateResponse(request=request, name="registr.html")

@app.get("/account", response_class=HTMLResponse)
async def get_account(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("account.html",
      {"request":request, "username": username, "date":datetime.now()})
