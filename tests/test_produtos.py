from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.produtos import Produtos
from schemas.schema_produtos import s_Produtos_out, s_Produtos_update_out


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

@pytest.mark.asyncio
async def test_delete_produto(client, categoria_teste, produto_teste, async_session):

    response = client.delete(f'/produtos/{produto_teste.id}') 

    produto_existe = await async_session.scalar(select(Produtos).where(Produtos.id == produto_teste.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Produto excluído'} 
    assert produto_existe is None

@pytest.mark.asyncio
async def test_atualizar_produto(client, categoria_teste, produto_teste, async_session):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'nome': 'teste',
        'descricao': 'outra_descricao aletaoria',
        'categoria_id': categoria_teste.id
    }

    response = client.patch(f'/produtos/{produto_teste.id}', json=dados)
    produto_bd = await async_session.scalar(select(Produtos).where(Produtos.id == produto_teste.id))
    produto_bd_ = s_Produtos_update_out.model_validate(produto_bd).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == produto_bd_

@pytest.mark.asyncio
async def test_atualizar_produto_outro_nome(client, categoria_teste, produto_teste, async_session):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'nome': f"{produto_teste.nome} + {produto_teste.nome}",
        'descricao': 'outra_descricao aletaoria',
        'categoria_id': categoria_teste.id
    }

    response = client.patch(f'/produtos/{produto_teste.id}', json=dados)

    produto_bd = await async_session.scalar(select(Produtos).where(Produtos.id == produto_teste.id))

    
    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome'] == produto_bd.nome
@pytest.mark.asyncio
async def test_atualizar_produto_produto_existente(client, categoria_teste, produto_teste, async_session):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'categoria_id':categoria_teste.id ,
        'nome': 'product_nielo',
        'descricao': 'teste',
        'preco': 10.0,
        'imagem_url': 'https://example.com/imagem.jpg',
        'ativo': True,
    }

    new_product = client.post('/produtos', json=dados)

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'nome': new_product.json()['nome'],
        'descricao': 'outra_descricao aletaoria',
        'categoria_id': categoria_teste.id
    }

    response = client.patch(f'/produtos/{produto_teste.id}', json=dados)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail':'Produto já cadastrado'}