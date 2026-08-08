from datetime import datetime, timezone
from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User
from schemas.schemas_usuario import s_Usuario_out

@pytest.mark.asyncio
async def test_create_user(client, async_session, empresa_criada):

    dados = {

        'nome': 'teste',
        'email': 'teste',
        'senha' : 'teste',
        'empresa_id' : empresa_criada.id,
        'filial_id' : None,
        'perfil' : 'TESTE'
    }

    response = client.post('/usuarios', json=dados)

    assert response.status_code == HTTPStatus.CREATED
    stmt = select(User).where(User.id == response.json()['id'])
    user_bd = await async_session.scalar(stmt)
    assert user_bd.id == response.json()['id']

@pytest.mark.asyncio
async def test_all_users(client, usuario_criado):

    response = client.get('/usuarios')

    validado =s_Usuario_out.model_validate(usuario_criado).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios':[validado]}