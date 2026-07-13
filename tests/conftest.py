import pytest_asyncio
import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from db.sessions import async_get_session
from main import app
from http import HTTPStatus
from models.empresas import Empresas

from sqlalchemy import StaticPool
from db.base import Base

@pytest_asyncio.fixture
async def client(async_session):

    async def get_async_session_override():
        return async_session

    with TestClient(app) as client:
        app.dependency_overrides[async_get_session] = get_async_session_override
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_session():

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def empresa_criada(async_session):
    
    empresa = Empresas(
        nome = "teste",
        centro_de_custo = 1,
        ativo = True
    )


    async_session.add(empresa)
    async_session.commit()
    async_session.refresh(empresa)
    return empresa