from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime
from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]                     #   int с функцией mapped_column

class User(Base):
    __tablename__= "users"

    id: Mapped[intpk]
    username: Mapped[str] 
    email: Mapped[str] 
    hash_pass: Mapped[str]

    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    comment_id: Mapped[str] = mapped_column(ForeignKey("comments.id"))

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] 
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    image_path: Mapped[str | None] 
    
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")


class Comment(Base):
    __tablename__="comments"

    id: Mapped[intpk]
    content: Mapped[str] 
    author_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.now)
    post_id = Column(Integer, ForeignKey('posts.id'))
    image_path: Mapped[str | None]

    author = relationship("User", back_populates="comments")
    posts = relationship("Post", back_populates="comments")
