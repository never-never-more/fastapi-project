from fastapi import FastAPI, Path, Query, Body, Request, Form
from fastapi.responses import  HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Cookie
from pydantic import BaseModel, field_validator, ValidationError

class LoginForm(BaseModel):
    username: str
    password: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html")

@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    return templates.TemplateResponse(request=request, name="contact.html")

@app.get("/login")
async def get_login(
    username: str = Form(...),
    password: str = Form(...)
                    ):
    form_data = LoginForm(
        username=username,
        password=password
    )
    return RedirectResponse("/", status_code=303)


@app.get("/registr", response_class=HTMLResponse)
async def get_registr(request: Request):
    return templates.TemplateResponse(request=request, name="registr.html")

