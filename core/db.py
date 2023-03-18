from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from .config import DB_NAME, DB_ROOT

Base = declarative_base()

class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


async_engine = create_async_engine(DB_ROOT + DB_NAME)
async_session = sessionmaker(async_engine, class_=AsyncSession)


async def create_database():
    async with async_engine.begin() as conn:
        async with async_session() as session:
            await conn.run_sync(Base.metadata.create_all)
