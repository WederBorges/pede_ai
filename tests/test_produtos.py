from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.produtos import Produtos
from schemas.schema_produtos import s_Produtos_out


@pytest.mark.asyncio
async def test_create_produto(client, async_session, categoria_teste):

    dados = {
        'categoria_id': categoria_teste.id,
        'nome': 'teste',
        'descricao': 'teste',
        'preco': 10.0,
        'imagem_url': 'https://example.com/imagem.jpg',
        'ativo': True,
    }

    response = client.post('/produtos', json=dados)

    stmt = select(Produtos).where(Produtos.id == response.json()['id'])
    produto_bd = await async_session.scalar(stmt)

    assert response.status_code == HTTPStatus.CREATED
    assert produto_bd.id == response.json()['id']


@pytest.mark.asyncio
async def test_ler_produtos(client, async_session, produto_teste):

    response = client.get('/produtos')

    produto_model = s_Produtos_out.model_validate(produto_teste).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': [produto_model]}


@pytest.mark.asyncio
async def test_create_produto_duplicado(
    client, async_session, produto_teste, categoria_teste
):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'categoria_id': categoria_teste.id,
        'nome': produto_teste.nome,
        'descricao': 'teste',
        'preco': 10.0,
        'imagem_url': 'https://example.com/imagem.jpg',
        'ativo': True,
    }

    response = client.post('/produtos', json=dados)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Produto já existe'}
