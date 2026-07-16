from datetime import datetime, timezone
from http import HTTPStatus

import pytest
from sqlalchemy import select

from models import Empresas
from schemas.schema_empresas import s_Empresas_create, s_Empresas_out


@pytest.mark.asyncio
async def test_leitura_empresas(client, empresa_criada):

    response = client.get('/empresas')
    empresa = s_Empresas_out.model_validate(empresa_criada).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'empresas': [empresa]}


@pytest.mark.asyncio
async def test_ler_uma_empresa(client, empresa_criada):

    response = client.get(f'/empresas/{empresa_criada.id}')
    empresa = s_Empresas_create.model_validate(empresa_criada).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == empresa


@pytest.mark.asyncio
async def test_create_empresa(client):

    response = client.post(
        '/empresas', json={'nome': 'string', 'centro_de_custo': 0, 'ativo': True}
    )

    datetime_json = response.json()['created_at']
    datetime_format = datetime.fromisoformat(datetime_json).date()

    assert response.status_code == HTTPStatus.CREATED
    assert datetime_format == datetime.now(tz=timezone.utc).date()


@pytest.mark.asyncio
async def test_delete_empresa(client, empresa_criada, async_session):

    response = client.delete(f'/empresas/{empresa_criada.id}')

    stmt = select(Empresas).where(Empresas.id == empresa_criada.id)
    exists_empresa = await async_session.scalar(stmt)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert exists_empresa is None
