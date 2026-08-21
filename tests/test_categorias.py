from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.categorias import Categoria
from schemas.schema_categorias import s_Categorias_out


@pytest.mark.asyncio
async def test_ler_categoria(client, categoria_teste):

    response = client.get('/categorias')

    model_categoria_criada = s_Categorias_out.model_validate(
        categoria_teste
    ).model_dump(mode='json')
    print(model_categoria_criada)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'categorias': [model_categoria_criada]}


@pytest.mark.asyncio
async def test_criar_categoria(client, async_session):

    dados = {
        'nome': 'categoria_teste',
        'descricao': 'descricao_teste',
        'ativo': True,
    }

    response = client.post('/categorias', json=dados)

    stmt = select(Categoria).where(Categoria.nome == dados['nome'])
    categoria_criada = await async_session.scalar(stmt)

    model_categoria_criada = s_Categorias_out.model_validate(
        categoria_criada
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == model_categoria_criada


@pytest.mark.asyncio
async def test_criar_categoria_duplicada(client, categoria_teste):

    dados = {
        'nome': categoria_teste.nome,
        'descricao': 'descricao_teste',
        'ativo': True,
    }

    response = client.post('/categorias', json=dados)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Categoria já existe'}


@pytest.mark.asyncio
async def test_ler_categoria_unica(client, categoria_teste):

    response = client.get(f'/categorias/{categoria_teste.id}')

    model_categoria_criada = s_Categorias_out.model_validate(
        categoria_teste
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == model_categoria_criada


@pytest.mark.asyncio
async def test_ler_categoria_unica_inexistente(client):

    response = client.get('/categorias/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Categoria não encontrada'}


@pytest.mark.asyncio
async def test_atualizar_categoria(client, categoria_teste, async_session):

    dados = {
        'nome': 'categoria_atualizada',
        'descricao': 'descricao_atualizada',
        'ativo': False,
    }

    response = client.patch(f'/categorias/{categoria_teste.id}', json=dados)

    stmt = select(Categoria).where(Categoria.id == categoria_teste.id)
    categoria_atualizada = await async_session.scalar(stmt)

    model_categoria_atualizada = s_Categorias_out.model_validate(
        categoria_atualizada
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == model_categoria_atualizada


@pytest.mark.asyncio
async def test_atualizar_categoria_inexistente(client):
    dados = {
        'nome': 'categoria_atualizada',
        'descricao': 'descricao_atualizada',
        'ativo': False,
    }

    response = client.patch('/categorias/999', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Categoria não encontrada'}


@pytest.mark.asyncio
async def test_atualizar_categoria_duplicada(client, categoria_teste, async_session):

    # Criar uma segunda categoria para testar a duplicidade
    dados_segunda_categoria = {
        'nome': 'categoria_segunda',
        'descricao': 'descricao_segunda',
        'ativo': True,
    }

    response_segunda = client.post('/categorias', json=dados_segunda_categoria)

    await async_session.refresh(categoria_teste)

    stmt = select(Categoria).where(Categoria.nome == dados_segunda_categoria['nome'])
    segunda_categoria_criada = await async_session.scalar(stmt)

    # Tentar atualizar a primeira categoria com o nome da segunda
    dados_atualizacao = {
        'nome': segunda_categoria_criada.nome,
        'descricao': 'descricao_atualizada',
        'ativo': False,
    }

    response_atualizacao = client.patch(
        f'/categorias/{categoria_teste.id}', json=dados_atualizacao
    )
    await async_session.refresh(categoria_teste)

    assert response_atualizacao.status_code == HTTPStatus.CONFLICT
    assert response_atualizacao.json() == {'detail': 'Categoria já existe'}


@pytest.mark.asyncio
async def test_atualizar_categoria_parcial(client, categoria_teste, async_session):

    dados = {
        'descricao': 'descricao_parcial',
    }

    response = client.patch(f'/categorias/{categoria_teste.id}', json=dados)

    stmt = select(Categoria).where(Categoria.id == categoria_teste.id)
    categoria_atualizada = await async_session.scalar(stmt)

    model_categoria_atualizada = s_Categorias_out.model_validate(
        categoria_atualizada
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == model_categoria_atualizada


@pytest.mark.asyncio
async def test_deletar_categoria(client, categoria_teste, async_session):

    response = client.delete(f'/categorias/{categoria_teste.id}')

    stmt = select(Categoria).where(Categoria.id == categoria_teste.id)
    categoria_existe = await async_session.scalar(stmt)

    assert response.status_code == HTTPStatus.OK
    assert categoria_existe is None
