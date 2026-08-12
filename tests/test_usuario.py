from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User
from models.empresas_e_filiais import Empresas, Filiais
from schemas.schemas_usuario import s_Usuario_out


@pytest.mark.asyncio
async def test_create_user(client, async_session, empresa_criada):

    dados = {
        'nome': 'teste',
        'email': 'teste',
        'senha': 'teste',
        'empresa_id': empresa_criada.id,
        'filial_id': None,
        'perfil': 'TESTE',
    }

    response = client.post('/usuarios', json=dados)

    assert response.status_code == HTTPStatus.CREATED
    stmt = select(User).where(User.id == response.json()['id'])
    user_bd = await async_session.scalar(stmt)
    assert user_bd.id == response.json()['id']


@pytest.mark.asyncio
async def test_all_users(client, usuario_criado):

    response = client.get('/usuarios')

    validado = s_Usuario_out.model_validate(usuario_criado).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': [validado]}


@pytest.mark.asyncio
async def test_user(client, usuario_criado, async_session):

    response = client.get(f'/usuarios/{usuario_criado.id}')

    validado = s_Usuario_out.model_validate(usuario_criado).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == validado


@pytest.mark.asyncio
async def test_update_user(client, usuario_criado, async_session):

    dados = {'nome': 'wederteste'}

    response = client.patch(f'/usuarios/{usuario_criado.id}', json=dados)

    userbd = await async_session.scalar(
        select(User).where(User.id == response.json()['id'])
    )
    user_bd = s_Usuario_out.model_validate(userbd).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert userbd.nome == dados['nome']


@pytest.mark.asyncio
async def test_delete_user(client, usuario_criado, async_session):

    response = client.delete(f'/usuarios/{usuario_criado.id}')

    userbd = await async_session.scalar(
        select(User).where(User.id == usuario_criado.id)
    )


    assert response.status_code == HTTPStatus.OK
    assert userbd is None

@pytest.mark.asyncio
async def test_usuario_inexistente(client, async_session, usuario_criado):

    response = client.get(f'/usuarios/{usuario_criado.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário inexistente'}

@pytest.mark.asyncio
async def test_filial_vinculada_usuario_inexistente(
    client, async_session, empresa_criada, filial_criada):

    await async_session.refresh(empresa_criada)
    await async_session.refresh(filial_criada)

    response = client.post('/usuarios', json={
        'nome': 'teste',
        'email': 'teste@example.com',
        'senha': 'teste123',
        'empresa_id': empresa_criada.id,
        'filial_id': filial_criada.id + 1,
        'perfil': 'TESTE'
    })

    print(response.json())
    # assert response.status_code == HTTPStatus.NOT_FOUND
    # assert response.json() == {'detail': 'Filial não encontrada'}