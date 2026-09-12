import os

os.environ.setdefault(
    'DATABASE_URL',
    'sqlite+aiosqlite:///:memory:',
)

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from db.base import Base
from db.sessions import async_get_session
from main import app
from models.categorias import Categoria
from models.empresas_e_filiais import Empresas, Filiais
from models.produtos import Produtos
from models.usuarios import User


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
        'sqlite+aiosqlite:///:memory:',
        connect_args={
            'check_same_thread': False,
        },
        poolclass=StaticPool,
    )

    @event.listens_for(engine.sync_engine, 'connect')
    def set_sqlite_pragma(
        dbapi_connection,
        connection_record,
    ):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await session.close()  # entender isso dps, mas copiei e colei
    await engine.dispose()


@pytest_asyncio.fixture
async def empresa_teste(async_session):

    empresa = Empresas(
        nome='empresa_teste',
        centro_de_custo=1,
        ativo=True,
    )

    async_session.add(empresa)
    await async_session.commit()
    await async_session.refresh(empresa)

    return empresa


@pytest_asyncio.fixture
async def filial_teste(
    async_session,
    empresa_teste,
):

    await async_session.refresh(empresa_teste)

    filial = Filiais(
        nome='filial_teste',
        empresa_id=empresa_teste.id,
        cidade='teste',
        estado='teste',
        ativo=True,
    )

    async_session.add(filial)
    await async_session.commit()
    await async_session.refresh(filial)

    return filial


@pytest_asyncio.fixture
async def usuario_teste(async_session, empresa_teste, filial_teste):

    await async_session.refresh(empresa_teste)

    user = User(
        nome='usuario_teste',
        email='teste@example.com',
        senha_hash='senha_teste',
        empresa_id=empresa_teste.id,
        filial_id=filial_teste.id,
        perfil='colaborador',
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def categoria_teste(async_session):

    categoria = Categoria(
        nome='categoria_teste',
        descricao='teste',
        ativo=True,
    )

    async_session.add(categoria)
    await async_session.commit()
    await async_session.refresh(categoria)

    return categoria


@pytest_asyncio.fixture
async def produto_teste(
    async_session,
    categoria_teste,
):

    produto = Produtos(
        categoria_id=categoria_teste.id,
        nome='produto_teste',
        descricao='teste',
        preco=10.0,
        imagem_url='https://example.com/imagem.jpg',
        ativo=True,
    )

    async_session.add(produto)
    await async_session.commit()
    await async_session.refresh(produto)

    return produto


@pytest_asyncio.fixture
async def produto_teste_inativo(
    async_session,
    categoria_teste,
):
    await async_session.refresh(categoria_teste)

    produto = Produtos(
        categoria_id=categoria_teste.id,
        nome='produto_teste_inativo',
        descricao='teste',
        preco=10.0,
        imagem_url='https://example.com/imagem.jpg',
        ativo=False,
    )

    async_session.add(produto)
    await async_session.commit()
    await async_session.refresh(produto)

    return produto


@pytest_asyncio.fixture
async def carrinho_teste(usuario_teste, async_session):
    from models.carrinho import Carrinho

    carrinho_teste = Carrinho(
        usuario_id=usuario_teste.id,
        filial_id=usuario_teste.filial_id,
    )

    async_session.add(carrinho_teste)
    await async_session.commit()
    await async_session.refresh(carrinho_teste)
    return carrinho_teste


@pytest_asyncio.fixture
async def carrinho_com_item_teste(carrinho_teste, produto_teste, async_session):
    from models.carrinho import CarrinhoItens

    carrinho_com_item_teste = CarrinhoItens(
        carrinho_id=carrinho_teste.id, produto_id=produto_teste.id, quantidade=1
    )

    async_session.add(carrinho_com_item_teste)
    await async_session.commit()
    await async_session.refresh(carrinho_com_item_teste)
    return carrinho_com_item_teste
