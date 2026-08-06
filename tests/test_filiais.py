from datetime import datetime, timezone
from http import HTTPStatus

import pytest
from sqlalchemy import select

from models import Filiais


@pytest.mark.asyncio
async def test_create_filial(client, empresa_criada, async_session):
    dados = {
        'nome': 'filial1',
        'empresa_id': empresa_criada.id,
        'cidade': 'cuiaba',
        'estado': 'mato grosso',
        'ativo': True,
    }

    response = client.post('/filiais', json=dados)

    datetime_json = response.json()['created_at']
    datetime_format = datetime.fromisoformat(datetime_json).date()
    dt_atual = datetime.now(tz=timezone.utc).date()

    stmt = select(Filiais).where(Filiais.nome == response.json()['nome'])

    filial_persistida = await async_session.scalar(stmt)

    assert response.status_code == HTTPStatus.CREATED
    assert datetime_format == dt_atual
    assert filial_persistida.nome == dados['nome']


@pytest.mark.asyncio
async def test_not_found_filial(client, empresa_criada):

    dados = {
        'nome': 'filial2',
        'empresa_id': empresa_criada.id + 1,
        'cidade': 'jaciara',
        'estado': 'mato grosso',
        'ativo': False,
    }

    response = client.post('/filiais', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_filial(client, async_session, filial_criada):

    response = client.delete(f'/filiais/{filial_criada.id}')

    stmt = select(Filiais).where(Filiais.id == filial_criada.id)
    filial_existe = await async_session.scalar(stmt)

    assert response.status_code == HTTPStatus.OK
    assert filial_existe is None


@pytest.mark.asyncio
async def test_delete_filial_not_found(client, async_session, filial_criada):

    response = client.delete(f'/filiais/{filial_criada.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_create_filial_Integrity_error(
    client, async_session, empresa_criada, filial_criada
):

    await async_session.refresh(empresa_criada)
    await async_session.refresh(filial_criada)

    dados = {
        'nome': filial_criada.nome,
        'empresa_id': empresa_criada.id,
        'cidade': 'jaciara',
        'estado': 'mato grosso',
        'ativo': False,
    }

    response = client.post('/filiais', json=dados)

    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.asyncio
async def test_update_filial(client, async_session, empresa_criada, filial_criada):

    await async_session.refresh(empresa_criada)
    await async_session.refresh(filial_criada)

    dados = {'nome': 'atualizando'}

    response = client.patch(f'/filiais/{filial_criada.id}', json=dados)

    stmt = select(Filiais).where(Filiais.id == filial_criada.id)
    filial = await async_session.scalar(stmt)


    assert response.status_code == HTTPStatus.OK
    assert filial.nome == dados['nome']


@pytest.mark.asyncio
async def test_get_not_found_filial(client, filial_criada):

    response = client.get(f'/filiais/{filial_criada.id+1}')
    assert response.status_code == HTTPStatus.NOT_FOUND 


@pytest.mark.asyncio
async def test_get_not_found_filial_empresa_notexists(client, filial_criada, empresa_criada, async_session):

    await async_session.refresh(empresa_criada)
    await async_session.refresh(filial_criada)
    
    dados = {'empresa_id': 0}
    response = client.patch(f'/filiais/{filial_criada.id}', json=dados)
    assert response.status_code == HTTPStatus.NOT_FOUND 


@pytest.mark.asyncio
async def test_update_integrity_error(client, filial_criada, empresa_criada, async_session):

    await async_session.refresh(empresa_criada)
    await async_session.refresh(filial_criada)


    dados =  {
        "nome":'filial2',
        "empresa_id":empresa_criada.id,
        "cidade":'teste',
        "estado":'teste',
        "ativo":True,
    }


    filial2 = client.post(f'/filiais', json=dados)

    # dados2 = {'nome':dados['nome'], 'empresa_id': empresa_criada}

    # response = client.patch(f'filiais/{filial_criada.id}')
    print(filial2.json()['id'])

    # emp2 = async_session.scalar(select(Filiais).weher(Filiais.id = dados.))

    # assert filial2.status_code == HTTPStatus.CREATED 
    # assert response.status_code == HTTPStatus.CONFLICT