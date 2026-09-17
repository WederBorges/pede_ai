import pytest
from models.pedidos import Pedidos

from http import HTTPStatus

from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_pedido(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste
    response = client.post(f'pedido/{carrinho.id}')
    

    carrinho_bd = async_session.scalar(select(Pedidos).where(Pedidos.id == response.json()['id']))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['id'] == carrinho_bd.id
