import json

import pytest
from models.pedidos import Pedidos, PedidoStatusHistorico
from models.enums_pedido import Status_Pedidos

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


@pytest.mark.asyncio
async def test_atualizar_status_pedido_APROVADO(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']
    
    # Atualiza o status do pedido para "APROVADO"
    response_update = client.patch(f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'})
    
    print(response_update.status_code)
    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.OK
    assert pedido_bd.status.value == 'APROVADO'


@pytest.mark.asyncio
async def test_atualizar_status_pedido_ETAPA_A_FRENTE(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']
    
    # Atualiza o status do pedido para "EM_SEPARACAO"
    response_update = client.patch(f'/pedido/{pedido_id}/status', json={'status': 'EM_SEPARACAO'})

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert pedido_bd.status.value == 'PENDENTE'



@pytest.mark.asyncio
async def test_atualizar_pedido_inexistente(client, async_session):

    response_update = client.patch(f'/pedido/{999999}/status', json={'status': 'APROVADO'})

    assert response_update.status_code == HTTPStatus.NOT_FOUND
    assert response_update.json()['detail'] == 'Pedido inexistente'


@pytest.mark.asyncio
async def test_historico_gravado(client, async_session, carrinho_com_item_teste):
    
    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']
    
    # Atualiza o status do pedido para "APROVADO"
    response_update = client.patch(f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'})
    
    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )


    # Verifica se o histórico foi gravado corretamente
    historico = await async_session.scalars(
            select(PedidoStatusHistorico)
            .where(PedidoStatusHistorico.pedido_id == pedido_id)
            .order_by(PedidoStatusHistorico.id)
    )

    statuses = [h.status for h in historico.all()]

    assert historico is not None
    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.OK
    assert statuses == [Status_Pedidos.PENDENTE, Status_Pedidos.APROVADO]


@pytest.mark.asyncio
async def test_atualizar_pedido_cancelado(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']
    
    # Atualiza o status do pedido para "CANCELADO"
    response_update = client.patch(f'/pedido/{pedido_id}/status', json={'status': 'CANCELADO'})
    
    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )



    
    # Atualiza pedido cancelado para aprovado
    response_update_teste_conflito = client.patch(f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'})


    historico = await async_session.scalars(
                select(PedidoStatusHistorico)
                .where(PedidoStatusHistorico.pedido_id == pedido_id)
                .order_by(PedidoStatusHistorico.id)
        )
    statuses = [h.status for h in historico.all()]


    esperado = (
        f'Pedido {pedido_bd.id} está {pedido_bd.status.value}, '
        'que é um estado final e não aceita novas mudanças.'
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.OK
    assert response_update_teste_conflito.status_code == HTTPStatus.CONFLICT
    assert pedido_bd.status.value == 'CANCELADO'
    assert statuses == [Status_Pedidos.PENDENTE, Status_Pedidos.CANCELADO]
    assert response_update_teste_conflito.json()['detail'] == esperado

@pytest.mark.asyncio
async def teste_criar_previsao_entrega(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste
    pedido_response = client.post(f'/pedido', json={'carrinho_id': carrinho.id})

    id_pedido = pedido_response.json()['id_pedido']
    pedido_aprovado = client.patch(f'/pedido/{id_pedido}/status', json={'status': 'APROVADO'})

    previsao_entrega = client.patch(f'pedido/{id_pedido}/previsao-entrega', json={'previsao_entrega': '01/12/2026'})

    print(pedido_response.json())
    print(id_pedido, "ID PEDIDO")
    print(pedido_aprovado.json())