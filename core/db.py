from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from .config import DB_NAME, DB_ROOT

class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)
# DB_ROOT = 'sqlite+aiosqlite:///./'
# DB_NAME = 'binance.db'

engine = create_async_engine('sqlite+aiosqlite:///./binance.db')
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def create_database():
    async with AsyncSessionLocal() as session:
        yield session
        # async with async_session() as session:
        #     await conn.run_sync(Base.metadata.create_all)
