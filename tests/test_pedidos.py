import pytest
from models.pedidos import Pedidos

from http import HTTPStatus

from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_pedido(client, async_session, carrinho_com_item_teste):
    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    print(response.json())  # ← temporário, só pra investigar
    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == response.json()['id_pedido'])
    )

    assert response.status_code == HTTPStatus.CREATED
    assert pedido_bd is not None
    assert response.json()['id_pedido'] == pedido_bd.id
    assert response.json()['usuario_id'] == pedido_bd.usuario_id
    assert response.json()['status'] == pedido_bd.status.value
