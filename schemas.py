from pydantic import BaseModel, EmailStr, validator

class LoginForm(BaseModel):
    username: str
    password: str
    remember_me: bool = False

    @validator("username")
    def username_length(cls, v):
        if len(v) < 3:
            raise ValueError("Username length too short")
        return v
    
