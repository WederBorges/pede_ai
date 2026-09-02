from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User
from models.carrinho import Carrinho
from schemas.schema_carrinho import s_Create_carrinho_out


@pytest.mark.asyncio
async def test_create_carrinho(client, async_session, usuario_teste, filial_teste):

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id
    }

    response = client.post('/carrinho', json=dados)

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    stmt = select(Carrinho).where(Carrinho.usuario_id == usuario_teste.id)
    carrinho_bd = await async_session.scalar(stmt)

    model_carrinho = s_Create_carrinho_out.model_validate(carrinho_bd).model_dump(mode='json')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == model_carrinho


@pytest.mark.asyncio
async def test_filial_inexistente(client, async_session, usuario_teste, filial_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': 9999,
        'usuario_id': usuario_teste.id
    }

    response = client.post('/carrinho', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Filial inexistente'}


@pytest.mark.asyncio
async def test_usuario_inexistente(client, async_session, usuario_teste, filial_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id + 1
    }

    response = client.post('/carrinho', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário inexistente'}

    