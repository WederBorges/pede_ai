from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.produtos import Produtos
from schemas.schema_catalogo import s_Catalogo_out

@pytest.mark.asyncio
async def test_ler_catalogo(client, categoria_teste, produto_teste, produto_teste_inativo):

    
    response = client.get('/catalogo')

    print(response.json())
    assert response.status_code == HTTPStatus.OK
    

@pytest.mark.asyncio
async def test_catalogo_filtro_categoria_sem_match(client, async_session,categoria_teste, produto_teste):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)
    dados = {
        'produto': produto_teste.nome,
        'categoria_id': categoria_teste.id + 1
    }
    response = client.get('/catalogo', params=dados)
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': []}


@pytest.mark.asyncio
async def test_produto_filtro_categoria_sem_match(client, async_session,categoria_teste, produto_teste):

    await async_session.refresh(categoria_teste)
    await async_session.refresh(produto_teste)

    dados = {
        'produto': produto_teste.nome  ,
        'categoria_id': categoria_teste.id + 1
    }
    response = client.get('/catalogo', params=dados)
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': []}


@pytest.mark.asyncio
async def test_catalogo_filtro_categoria_com_match(client, async_session,categoria_teste, produto_teste):

    await async_session.refresh(categoria_teste)

    dados = {
        'categoria_id': categoria_teste.id
    }

    response = client.get('/catalogo', params=dados)

    produto = await async_session.scalar(
        select(Produtos)
        .where(
            Produtos.categoria_id == response.json()['produtos'][0]['categoria_id']
            )
        )

    produto_model = s_Catalogo_out.model_validate(produto).model_dump(mode='json')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': [produto_model]}


@pytest.mark.asyncio
async def test_produto_filtro_com_match(client, async_session,categoria_teste, produto_teste):

    await async_session.refresh(produto_teste)

    dados = {
        'produto': produto_teste.nome
    }

    response = client.get('/catalogo', params=dados)
    

    produto = await async_session.scalar(
        select(Produtos)
        .where(
            Produtos.nome.ilike(
                f'%{response.json()['produtos'][0]['nome']}%')
            )
        )

    produto_model = s_Catalogo_out.model_validate(produto).model_dump(mode='json')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': [produto_model]}


@pytest.mark.asyncio
async def test_produto_string_parcial_filtro_com_match(client, async_session,categoria_teste, produto_teste):

    await async_session.refresh(produto_teste)

    nome = produto_teste.nome
    dados = {
        'produto': nome[0:int(round(len(nome)/2))]
    }

    response = client.get('/catalogo', params=dados)
    

    produto = await async_session.scalar(
        select(Produtos)
        .where(
            Produtos.nome.ilike(
                f'%{response.json()['produtos'][0]['nome']}%')
            )
        )

    produto_model = s_Catalogo_out.model_validate(produto).model_dump(mode='json')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': [produto_model]}


