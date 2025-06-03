from typing import Annotated
from fastapi import FastAPI, Request, Form, status, Depends, HTTPException, UploadFile, File
from fastapi.responses import  HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

from sqlalchemy import select
import uvicorn
from schemas import LoginSchema, RegistrSchema
from passlib.context import CryptContext
from database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import Comment, User, Post
import os
import uuid


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SessionDep = Annotated[AsyncSession, Depends(get_db)]                       #   Создаем переменную запуска сессий

#   Домашняя страница -----------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, tags=["Home"], summary="get home page")  #   Request — это класс из модуля fastapi,
async def get_home(     request: Request,
                        db: SessionDep,
                        show_form: bool = False             ):              #   который предоставляет доступ к:
    
    username = request.cookies.get("username")                              #   headers, cookies, form(), body() и т.д.
    posts = db.execute(select(Post).order_by(Post.date.desc()).limit(10).all())

    return templates.TemplateResponse("home.html",
      {     "request":request,
            "username": username,
            "posts":posts,
            "date":datetime.now(),
            "show_form":show_form       })

#   Создание поста -------------------------------------------------------------------------------------------------------

@app.post("/posts")
async def create_post(  request: Request,
                        db: SessionDep,   
                        title: str = Form(...),
                        content: str = Form(...),
                        image: UploadFile = File(None),
                        ):
    
    username = request.cookies.get("username")
    if not username:
        response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        return response
    
    image_path = None
    if image and image.filename:
        # Генерируем уникальное имя файла
        file_ext = os.path.splitext(image.filename)[1]  #   1st part file name 
        file_name = f"{uuid.uuid4()}{file_ext}"         #   uuid + 1st part
        file_path = os.path.join(UPLOAD_DIR, file_name) #   full path to file
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
            image_path = f"/static/uploads/{file_name}"


    author = db.query(User).filter(User.username == username).first()
    new_post = Post(    title = title,
                        content = content,
                        author_id = author.id,
                        image_path = image_path     )
    
    db.add(new_post)
    db.commit()
    return RedirectResponse("/", status_code=303)

# Удаление поста --------------------------------------------------------------------------------------------------------

@app.post("/posts/{post_id}/delete")
async def delete_post(      post_id: int,
                            request: Request,
                            db: SessionDep      ):
    
    username = request.cookies.get("username")
    if not username:
        response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        return response
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return response

    author = db.query(User).filter(User.username == username).first()
    if author.id != post.author_id:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    if post.image_path:
        try:
            os.remove(f"static{post.image_path.split('static')[-1]}")
        except Exception as e:
            response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
            return response
        
    db.delete(post)
    db.commit()
    return RedirectResponse("/", status_code=303)

#   Страница редактирования поста   ---------------------------------------------------------------------------------------

@app.get("/posts/{post_id}/edit")
async def get_edit_post(    post_id: int,
                            request: Request,
                            db: SessionDep   ):              #   который предоставляет доступ к:
    
    username = request.cookies.get("username")                              #   headers, cookies, form(), body() и т.д.
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("post_edit.html",
      {     "request":request,
            "username": username,
            "post":post             })

#   Редактирование поста    ----------------------------------------------------------------------------------------------

@app.post("/posts/{post_id}/edit")
async def edit_post(    post_id: int,
                        request: Request,
                        db: SessionDep,
                        title: str = Form(...),
                        content: str = Form(...),
                        image: UploadFile = File(None),
                        ):

    username = request.cookies.get("username")
    post = db.query(Post).filter(Post.id == post_id).first()
    author = db.query(User).filter(User.username == username).first()
    if not post:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    if not username or (author.id != post.id):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    
    if image and image.filename:
        if post.image_path:
            try:
                os.remove(f"static{post.image_path.split('/static')[-1]}")
            except Exception as e:
                print(f"Error deleting old image: {e}")
        
        # Генерируем уникальное имя файла
        file_ext = os.path.splitext(image.filename)[1]  #   1st part file name 
        file_name = f"{uuid.uuid4()}{file_ext}"         #   uuid + 1st part
        file_path = os.path.join(UPLOAD_DIR, file_name) #   full path to file
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        
        post.image_path = f"/static/uploads/{file_name}"
    
    post.title = title
    post.content = content
    post.updated_at = datetime.utcnow()
    
    db.commit()
    
    return RedirectResponse("/", status_code=303)



#   Страница поста -------------------------------------------------------------------------------------------------------

@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def get_post(     post_id: int,
                        request: Request,
                        db: SessionDep   ):
    
    username = request.cookies.get("username")
    post = db.query(Post).filter(Post.id == post_id).first()
    comments = db.query(Comment).filter(Comment.post_id == post.id).all()
    return templates.TemplateResponse("post.html", {
        "request" : request,
        "username": username,
        "post": post,
        "comments": comments
    })

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

@app.get("/login", response_class=HTMLResponse, tags=["Login"], summary="get login page")             #   Получить HTML страницу логин
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login", tags=["Login"], summary="Login function")                                         #   Создать POST запрос 
async def post_login(   user: LoginSchema,
                        db: SessionDep      ):
    
    db_user = await db.execute(select(User).where(User.username == user.username))
    if not db_user or not verify_pass(user.password, db_user.hash_pass):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": "Login sucecssful", "username": db_user.username }



# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pass(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

def get_pass_hash(passw):
    return pwd_context.hash(passw)


#   Регистрация ---------------------------------------------------------------------------------------------

@app.get("/registr", response_class=HTMLResponse, tags=["Registration"], summary="Get Registration page")
async def get_registr(request: Request):
    return templates.TemplateResponse(request=request, name="registr.html")

@app.post("/registr", tags=["Registration"], summary="Add new User to database")            #   Пост запрос на регистрацию
async def registr(  new_user: RegistrSchema, 
                    db: SessionDep              ):
    
    db_user = await db.execute(select(User).where(  (User.username == new_user.username)
                                                    | (User.email == new_user.email)         ))
    
    scalar_user = db_user.scalars().first()                                                 #   Переводим в скалярный вид
    if scalar_user:
        if scalar_user.username == new_user.username:
            raise HTTPException(status_code=400, detail="Username allready exist!")
        else:
            raise HTTPException(status_code=400, detail="E-mail allready exist!")
        
    hpass = get_pass_hash(new_user.password)

    new_user = User(    username = new_user.username,
                        email = new_user.email,
                        hash_pass = hpass              )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



#   Личный Кабинет ------------------------------------------------------------------------------------------

@app.get("/account", response_class=HTMLResponse, tags=["Personal Account"], summary="link to personal cabinet")
async def get_account(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("account.html",
      {"request":request, "username": username, "date":datetime.now()})

@app.post("/logout", tags=["Personal Account"], summary="logout button function")             #   Создать POST запрос 
async def logout(request: Request):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("username")
    return response

#   Функция для создания пустых таблиц БД -------------------------------------------------------------------

@app.post("/create_db", tags=["Data Base"], summary="delete and create db file")                         
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"Status": "Ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)