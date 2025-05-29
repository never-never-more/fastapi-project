from ast import For
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime
from typing import Annotated, Optional


intpk = Annotated[int, mapped_column(primary_key=True)]                     #   новый тип int уже с функцией mapped_column

class User(Base):
    __tablename__= "users"

    id: Mapped[intpk]
    username: Mapped[str] 
    email: Mapped[str] 
    hash_pass: Mapped[str]


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] 
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    image_path: Mapped[Optional[str]]   # "Опционально" либо стр либо ничего (None) 



class Comment(Base):
    __tablename__="comments"

    id: Mapped[intpk]
    content: Mapped[str] 
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    image_path: Mapped[Optional[str]]

