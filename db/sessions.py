import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL não está definido no arquivo .env')

async_engine = create_async_engine(DATABASE_URL)

session_maker = async_sessionmaker(bind=async_engine)


async def async_get_session():
    async with session_maker() as async_session:
        yield async_session
