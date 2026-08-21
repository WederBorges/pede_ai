from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.produtos import Produtos

@pytest.mark.asyncio
async def test_create_produto(client, async_session, categoria_teste):
    
    dados = {

    'categoria_id': categoria_teste.id,
    'nome': 'teste',
    'descricao': 'teste',
    'preco': 10.0,
    'imagem_url': 'https://example.com/imagem.jpg',
    'ativo': True
    }


    response = client.post('/produtos', json=dados)

    stmt = select(Produtos).where(Produtos.id == response.json()['id'])
    produto_bd = await async_session.scalar(stmt)
    

    assert response.status_code == HTTPStatus.CREATED
    assert produto_bd.id == response.json()['id']

@pytest.mark.async_session
async def ler_produtos(client, async_session, categoria_teste):

    dados = {
        'categoria_id': categoria_teste.id,
        'nome': 'teste',
        'descricao': 'teste',
        'preco': 10.0,
        'imagem_url': 'https://example.com/imagem.jpg',
        'ativo': True
    }

    response = client.post('/produtos', json=dados)

    response = client.get('/produtos')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['produtos']) > 0

    