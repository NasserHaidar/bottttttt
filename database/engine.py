import os
from database.models.user import Base

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# Create the SQLAlchemy engine
engine = create_async_engine(os.getenv('DB_LITE') , echo=True)

# Create an async session maker
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)