from fastapi import FastAPI, Path, Query, Body, Request, Form, status, Depends, HTTPException
from fastapi.responses import  HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from schemas import UserResponse
from passlib.context import CryptContext
from dependencies import get_db
from sqlalchemy.orm import Session
from models import User, Post


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#   Домашняя страница -----------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)                                  #   Request — это класс из модуля fastapi,
async def get_home(request: Request,
                   db: Session = Depends(get_db)):                                       #   который предоставляет доступ к:
    username = request.cookies.get("username")                              #   headers, cookies, form(), body() и т.д.
    posts = db.query(Post).order_by(Post.date.desc()).limit(10).all()

    return templates.TemplateResponse("home.html",
      {"request":request, "username": username, "posts":posts, "date":datetime.now()})

@app.post("/posts")
async def create_post(  request: Request,
                        title: str = Form(...),
                        content: str = Form(...),
                        db: Session = Depends(get_db)):
    
    username = request.cookies.get("username")
    if not username:
        response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        return response
    
    author = db.query(User).filter(User.username == username).first()
    new_post = Post(    title = title,
                        content = content,
                        author_id = author.id   )
    db.add(new_post)
    db.commit()
    return RedirectResponse("/", status_code=303)

#   Вкладки --------------------------------------------------------------------------------------------------------------

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


#   Авторизация --------------------------------------------------------------------------------------------

@app.get("/login", response_class=HTMLResponse)                             #   Получить HTML страницу логин
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")                                                         #   Создать POST запрос 
async def post_login(   request: Request,
                        db: Session = Depends(get_db),
                        username: str = Form(...),
                        password: str = Form(...)       ):
    
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_pass(password, user.hash_pass):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверное имя пользователя или пароль",
            },
            status_code=401
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


#   Регистрация ---------------------------------------------------------------------------------------------

@app.get("/registr", response_class=HTMLResponse)
async def get_registr(request: Request):
    return templates.TemplateResponse(request=request, name="registr.html")

@app.post("/registr", response_model=UserResponse)

async def registr(  request: Request,
                    username: str = Form(...),
                    email: str = Form(...),
                    password: str = Form(...),
                    db: Session = Depends(get_db)  ):
    
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return templates.TemplateResponse(
            "registr.html",
            {
                "request": request,
                "error": "Пользователь уже существует",
            },
            status_code=401
        )
    db_email = db.query(User).filter(User.email == email).first()
    if db_email:
        return templates.TemplateResponse(
            "registr.html",
            {
                "request": request,
                "error": "email уже используется",
            },
            status_code=401
        )
    if len(username) < 3 or len(email) < 5 or len(password) < 3:
        return templates.TemplateResponse(
            "registr.html",
            {
                "request": request,
                "error": "Минимальная длина username - 3, email - 5, password - 3",
            },
            status_code=401
        )
    hpass = get_pass_hash(password)

    new_user = User(    username=username,
                        email=email,
                        hash_pass=hpass     )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)     #   редирект на домашнюю страницу
    response.set_cookie(key="username", value=username)                     #   с юзернеймом
    return response


#   Личный Кабинет ------------------------------------------------------------------------------------------

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