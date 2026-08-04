from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import Query
import pytest
from sqlalchemy import select

from models import Filiais
from schemas.schema_filiais import s_Filiais_create, s_Filiais_out


@pytest.mark.asyncio
async def test_create_filial(client ,empresa_criada, async_session):
    dados = {
        'nome': "filial1",
        'empresa_id':empresa_criada.id,
        'cidade':'cuiaba',
        'estado':'mato grosso',
        'ativo': True
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
        'nome': "filial2",
        'empresa_id':empresa_criada.id + 1,
        'cidade':'jaciara',
        'estado':'mato grosso',
        'ativo': False
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
    

