from http import HTTPStatus
from datetime import datetime

import pytest

@pytest.mark.asyncio
async def test_leitura_empresas(client, empresa_criada):

    response = client.get('/empresas')
    

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"empresas":[
        {'nome':'teste',
         'centro_de_custo':1,
         'ativo': True}
    ]}

@pytest.mark.asyncio
async def test_create_empresa(client):

    response = client.post(
        '/empresas', json={'nome': 'string', 'centro_de_custo': 0, 'ativo': True}
    )

    datetime_json = response.json()['created_at']
    datetime_format = datetime.strptime(datetime_json, "%Y-%m-%dT%H:%M:%S").date()
 

    assert response.status_code == HTTPStatus.CREATED
    assert datetime_format == datetime.now().date()

