from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hash_pass = Column(String)

    posts = relationship("Post", back_populates="author")
    

class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.now)
    author = relationship("User", back_populates="posts")
