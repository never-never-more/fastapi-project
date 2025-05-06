from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class LoginForm(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_length(cls, v):                            #   cls — это ссылка на сам класс (в данном случае на класс LoginForm).
                                                            #   Он аналогичен self, но работает на уровне класса, а не экземпляра.
        if len(v) < 3:
            raise ValueError("Username length too short")
        return v
    
    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 3:
            raise ValueError("Password length too short")
        return v

class RegistrForm(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    def username_length(cls, v):                            #   cls — это ссылка на сам класс (в данном случае на класс LoginForm).
                                                            #   Он аналогичен self, но работает на уровне класса, а не экземпляра.
        if len(v) < 3:
            raise ValueError("Username length too short")
        return v

    @field_validator("email")
    def email_length(cls, v):
        if len(v) < 5:
            raise ValueError("Email length too short")
        return v

    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 3:
            raise ValueError("Password length too short")
        return v


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        #   объектно-реляционное отображение
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True

