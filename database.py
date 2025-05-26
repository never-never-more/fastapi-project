from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///test.db")             #   Создаем движок БД
new_session = async_sessionmaker(engine, expire_on_commit=False)        #   Создаем асинхронную сессию движка БД

async def get_db():                                                     #   Функция запуска сессии подключения к БД
    async with new_session() as session:
        yield session

class Base(DeclarativeBase):                                            #   Создаем класс для насследования других классов 
    pass                                                                #   с моделью БД

