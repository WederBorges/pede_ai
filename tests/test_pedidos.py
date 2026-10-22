from datetime import date, timedelta
from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.enums_pedido import Status_Pedidos
from models.pedidos import Pedidos, PedidoStatusHistorico


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
async def test_create_pedido_carrinho_sem_item(client, async_session, carrinho_teste):

    dados = {'carrinho_id': carrinho_teste.id}

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

    response = client.post(
        '/pedido/', json={'carrinho_id': carrinho_com_item_teste.carrinho_id + 9999}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert (
        response.json()['detail']
        == 'Carrinho não encontrado. Verifique se o carrinho existe.'
    )


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
        select(Pedidos).where(Pedidos.id == response.json()['id_pedido'])
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response2.status_code == HTTPStatus.OK
    assert response2.json()['id_pedido'] == response_bd.id


@pytest.mark.asyncio
async def test_atualizar_status_pedido_APROVADO(
    client, async_session, carrinho_com_item_teste
):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']

    # Atualiza o status do pedido para "APROVADO"
    response_update = client.patch(
        f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'}
    )

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.OK
    assert pedido_bd.status.value == 'APROVADO'


@pytest.mark.asyncio
async def test_atualizar_status_pedido_ETAPA_A_FRENTE(
    client, async_session, carrinho_com_item_teste
):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']

    # Atualiza o status do pedido para "EM_SEPARACAO"
    response_update = client.patch(
        f'/pedido/{pedido_id}/status', json={'status': 'EM_SEPARACAO'}
    )

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert pedido_bd.status.value == 'PENDENTE'


@pytest.mark.asyncio
async def test_atualizar_pedido_inexistente(client, async_session):

    response_update = client.patch(
        f'/pedido/{999999}/status', json={'status': 'APROVADO'}
    )

    assert response_update.status_code == HTTPStatus.NOT_FOUND
    assert response_update.json()['detail'] == 'Pedido inexistente'


@pytest.mark.asyncio
async def test_historico_gravado(client, async_session, carrinho_com_item_teste):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']

    # Atualiza o status do pedido para "APROVADO"
    response_update = client.patch(
        f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'}
    )

    await async_session.scalar(
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
async def test_atualizar_pedido_cancelado(
    client, async_session, carrinho_com_item_teste
):

    carrinho = carrinho_com_item_teste

    response = client.post('/pedido/', json={'carrinho_id': carrinho.carrinho_id})

    pedido_id = response.json()['id_pedido']

    # Atualiza o status do pedido para "CANCELADO"
    response_update = client.patch(
        f'/pedido/{pedido_id}/status', json={'status': 'CANCELADO'}
    )

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_id)
    )

    # Atualiza pedido cancelado para aprovado
    response_update_teste_conflito = client.patch(
        f'/pedido/{pedido_id}/status', json={'status': 'APROVADO'}
    )

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


@pytest.mark.parametrize(
    ('pedido_com_status', 'http_esperado'),
    [
        (Status_Pedidos.PENDENTE.value, HTTPStatus.CONFLICT),
        (Status_Pedidos.APROVADO.value, HTTPStatus.OK),
        (Status_Pedidos.EM_SEPARACAO.value, HTTPStatus.OK),
        (Status_Pedidos.ENVIADO.value, HTTPStatus.OK),
        (Status_Pedidos.ENTREGUE.value, HTTPStatus.CONFLICT),
        (Status_Pedidos.CANCELADO.value, HTTPStatus.CONFLICT),
    ],
    indirect=['pedido_com_status'],
)
@pytest.mark.asyncio
async def test_criar_previsao_entrega(
    client, async_session, pedido_com_status, http_esperado
):

    status_inicial = pedido_com_status.status

    data_futura = date.today() + timedelta(days=7)

    previsao_entrega = client.patch(
        f'pedido/{pedido_com_status.id}/previsao-entrega',
        json={'previsao_entrega': f'{data_futura}'},
    )

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_com_status.id)
    )

    if http_esperado == HTTPStatus.OK:
        assert data_futura == pedido_bd.previsao_entrega
        assert data_futura.isoformat() == previsao_entrega.json()['previsao_entrega']
    else:
        assert pedido_bd.previsao_entrega is None

    assert previsao_entrega.status_code == http_esperado
    assert pedido_bd.status == status_inicial


# ajustar teste de espelho comparando o msm objeto .status com ele mesmo ####


@pytest.mark.asyncio
async def test_previsao_entrega_pedido_inexistente(client, pedido_com_status):

    data_futura = date.today() + timedelta(days=7)

    response = client.patch(
        f'/pedido/{pedido_com_status.id + 9999}/previsao-entrega',  # gera id inexistente
        json={'previsao_entrega': f'{data_futura}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ('pedido_com_status', 'att_status', 'http_esperado', 'status_esperado'),
    [
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.PENDENTE,
        ),
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.OK,
            Status_Pedidos.APROVADO,
        ),
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.PENDENTE,
        ),
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.PENDENTE,
        ),
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.PENDENTE,
        ),
        (
            Status_Pedidos.PENDENTE.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.OK,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.APROVADO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.APROVADO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.OK,
            Status_Pedidos.EM_SEPARACAO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.APROVADO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.APROVADO,
        ),
        (
            Status_Pedidos.APROVADO.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.OK,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.EM_SEPARACAO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.EM_SEPARACAO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.EM_SEPARACAO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.OK,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.EM_SEPARACAO,
        ),
        (
            Status_Pedidos.EM_SEPARACAO.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.OK,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.OK,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENVIADO.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENVIADO,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.ENTREGUE.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.ENTREGUE,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.PENDENTE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.APROVADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.EM_SEPARACAO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.ENVIADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.ENTREGUE,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
        (
            Status_Pedidos.CANCELADO.value,
            Status_Pedidos.CANCELADO,
            HTTPStatus.CONFLICT,
            Status_Pedidos.CANCELADO,
        ),
    ],
    indirect=['pedido_com_status'],
)
@pytest.mark.asyncio
async def test_troca_status_parametrize(
    async_session,
    client,
    att_status,
    status_esperado,
    pedido_com_status,
    http_esperado,
):

    st = {'status': att_status}
    response = client.patch(f'/pedido/{pedido_com_status.id}/status', json=st)

    pedido_bd = await async_session.scalar(
        select(Pedidos).where(Pedidos.id == pedido_com_status.id)
    )

    assert http_esperado == response.status_code
    assert pedido_bd.status == status_esperado
