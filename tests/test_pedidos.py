import pytest
from models.pedidos import Pedidos

from http import HTTPStatus

from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_pedido(client, async_session, carrinho_com_item_teste):
    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == response.json()['id_pedido'])
    )

    assert response.status_code == HTTPStatus.CREATED
    assert pedido_bd is not None
    assert response.json()['id_pedido'] == pedido_bd.id
    
    assert response.json()['usuario_id'] == pedido_bd.usuario_id
    assert response.json()['status'] == pedido_bd.status.value


@pytest.mark.asyncio
async def test_create_pedido_carrinho_sem_item(
    client, async_session, carrinho_teste):

    dados = {
        'carrinho_id': carrinho_teste.id
    }
    
    response = client.post('/pedido/', json=dados)

    assert response.status_code == HTTPStatus.BAD_REQUEST

@pytest.mark.asyncio
async def test_create_pedido_ja_existe(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste.carrinho_id
    response1 = client.post('/pedido/', json={'carrinho_id': carrinho})
    response2 = client.post('/pedido/', json={'carrinho_id': carrinho})

    
    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == response1.json()['id_pedido'])
    )
    
    assert response1.status_code == HTTPStatus.CREATED
    assert response2.status_code == HTTPStatus.CONFLICT
    assert pedido_bd is not None
    assert response1.json()['id_pedido'] == pedido_bd.id
    assert str(response1.json()['id_pedido']) in response2.json()['detail']


@pytest.mark.asyncio
async def test_create_pedido_inexiste(client, async_session, carrinho_com_item_teste):

    response = client.post('/pedido/', json={'carrinho_id':carrinho_com_item_teste.carrinho_id + 9999})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == "Carrinho não encontrado. Verifique se o carrinho existe."


@pytest.mark.asyncio
async def test_ler_pedido_inexistente(client, carrinho_com_item_teste):

    response = client.get(f'/pedido/{carrinho_com_item_teste.carrinho_id + 999}')

    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_ler_um_pedido(client, carrinho_com_item_teste, async_session):

    carrinho = carrinho_com_item_teste
    
    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    response2 = client.get(f'/pedido/{response.json()["id_pedido"]}')

    response_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == response.json()['id_pedido']))

    assert response.status_code == HTTPStatus.CREATED
    assert response2.status_code == HTTPStatus.OK
    assert response2.json()['id_pedido'] == response_bd.id