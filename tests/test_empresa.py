from http import HTTPStatus
from schemas.schema_empresas import s_Empresas_create
import pytest

@pytest.mark.asyncio
async def test_tempresas(client):
    
    response = client.post(
        '/empresas',
        json={
        "nome": "string",
        "centro_de_custo": 0,
        "ativo": True
    })

    assert response.status_code == HTTPStatus.CREATED
    