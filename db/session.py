import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv

import os

load_dotenv()


async_engine = create_async_engine(os.getenv("DATABASE_URL"))

async def async_get_session():

    async with AsyncSession(async_engine) as async_session:
        yield async_session

async def testar():
    async with async_engine.connect() as conn:
        print("conexão ok")

asyncio.run(testar())