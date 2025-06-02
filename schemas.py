from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Здесь создаются классы моделей типа Pydantic
# которые нужны для валидации получаемых данных
#  
class LoginSchema(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)

class RegistrSchema(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=3)


class UserResponse(BaseModel):
    id: int
    username: str = Field(min_length=3)
    email: EmailStr

    class Config:
        #   объектно-реляционное отображение
        from_attributes = True

class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    content: str

class PostResponse(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=20)
    content: str
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True

