import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

async_engine = create_async_engine(os.getenv('DATABASE_URL'))

session_maker = async_sessionmaker(bind=async_engine)


async def async_get_session():
    async with session_maker() as async_session:
        yield async_session
