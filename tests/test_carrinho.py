from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User


@pytest.mark.asyncio
async def test_create_carrinho(client, async_session, usuario_teste, filial_teste):

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id
    }


    response = client.post('/carrinho', json=dados)

    print(response.json())