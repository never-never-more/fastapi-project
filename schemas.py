from pydantic import BaseModel, EmailStr, field_validator

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

