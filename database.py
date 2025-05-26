from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///test.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

