from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column() 
    email: Mapped[str] = mapped_column() 
    hash_pass: Mapped[str] = mapped_column() 

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__="posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column() 
    content: Mapped[str] = mapped_column() 
    author_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.now)
    image_path: Mapped[str] = mapped_column() 
    
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")


class Comment(Base):
    __tablename__="comments"

    id: Mapped[int] = mapped_column(primary_key=True) 
    content: Mapped[str] = mapped_column() 
    author_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.now)
    post_id = Column(Integer, ForeignKey('posts.id'))

    author = relationship("User", back_populates="comments")
    posts = relationship("Post", back_populates="comments")
