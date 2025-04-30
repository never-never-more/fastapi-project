from fastapi import FastAPI, Path, Query, Body, Request, Form, status, Depends, HTTPException
from fastapi.responses import  HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Cookie
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime
from schemas import LoginForm, UserCreate, UserResponse
from passlib.context import CryptContext
from dependencies import get_db
from sqlalchemy.orm import Session
from models import User


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


#   Авторизация
@app.get("/login", response_class=HTMLResponse)                             #   Получить HTML страницу логин
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")                                                         #   Создать POST запрос 
async def post_login(   db: Session = Depends(get_db),
                        username: str = Form(...),
                        password: str = Form(...)   ):
    
    form_data = LoginForm(  username=username,                              #   Создать логин форму
                            password=password   )
    user = db.query(User).filter(User.username == username).first
    if not user or not verify_pass(password, user.hash_pass):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)     #   редирект на домашнюю страницу
    response.set_cookie(key="username", value=username)                     #   с юзернеймом
    return response 



# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pass(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

def get_pass_hash(passw):
    return pwd_context.hash(passw)

#   Регистрация
@app.get("/registr", response_class=HTMLResponse)
async def get_registr(request: Request):
    return templates.TemplateResponse(request=request, name="registr.html")

@app.post("/registr", response_model=UserResponse)
async def registr(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pass = get_pass_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_pass=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#   Личный Кабинет
@app.get("/account", response_class=HTMLResponse)
async def get_account(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("account.html",
      {"request":request, "username": username, "date":datetime.now()})

@app.post("/logout")                                                        #   Создать POST запрос 
async def logout(request: Request):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("username")
    return response