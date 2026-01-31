from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os


engine = create_async_engine("sqlite+aiosqlite:///shifoxona.db", echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session


MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)