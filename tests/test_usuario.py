from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User
from schemas.schemas_usuario import s_Usuario_out


@pytest.mark.asyncio
async def test_create_user(client, async_session, empresa_teste):

    dados = {
        'nome': 'teste',
        'email': 'teste',
        'senha': 'teste',
        'empresa_id': empresa_teste.id,
        'filial_id': None,
        'perfil': 'TESTE',
    }

    response = client.post('/usuarios', json=dados)

    assert response.status_code == HTTPStatus.CREATED
    stmt = select(User).where(User.id == response.json()['id'])
    user_bd = await async_session.scalar(stmt)
    assert user_bd.id == response.json()['id']


@pytest.mark.asyncio
async def test_all_users(client, usuario_teste):

    response = client.get('/usuarios')

    validado = s_Usuario_out.model_validate(usuario_teste).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': [validado]}


@pytest.mark.asyncio
async def test_user(client, usuario_teste, async_session):

    response = client.get(f'/usuarios/{usuario_teste.id}')

    validado = s_Usuario_out.model_validate(usuario_teste).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == validado


@pytest.mark.asyncio
async def test_update_user_empresa(client, usuario_teste, async_session):

    dados = {'nome': 'wederteste', 'empresa_id': usuario_teste.empresa_id}

    response = client.patch(f'/usuarios/{usuario_teste.id}', json=dados)
    userbd = await async_session.scalar(
        select(User).where(User.id == response.json()['id'])
    )

    assert response.status_code == HTTPStatus.OK
    assert userbd.nome == dados['nome']


@pytest.mark.asyncio
async def test_update_user_filial(
    client, usuario_teste, async_session, filial_teste, empresa_teste
):

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste)
    await async_session.refresh(empresa_teste)

    dados = {'nome': 'wederteste', 'filial_id': filial_teste.id}

    response = client.patch(f'/usuarios/{usuario_teste.id}', json=dados)

    userbd = await async_session.scalar(
        select(User).where(User.id == response.json()['id'])
    )

    assert response.status_code == HTTPStatus.OK
    assert userbd.nome == dados['nome']


@pytest.mark.asyncio
async def test_update_user_filial_inexistente(
    client, usuario_teste, async_session, filial_teste, empresa_teste
):
    await async_session.refresh(empresa_teste)
    await async_session.refresh(filial_teste)
    await async_session.refresh(usuario_teste)

    filial_id = filial_teste.id
    usuario_id = usuario_teste.id

    dados = {'nome': 'wederteste', 'filial_id': filial_id + 999}

    response = client.patch(f'/usuarios/{usuario_id}', json=dados)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Filial inexistente'}


@pytest.mark.asyncio
async def test_delete_user(client, usuario_teste, async_session):

    response = client.delete(f'/usuarios/{usuario_teste.id}')

    userbd = await async_session.scalar(
        select(User).where(User.id == usuario_teste.id)
    )

    assert response.status_code == HTTPStatus.OK
    assert userbd is None


@pytest.mark.asyncio
async def test_usuario_inexistente(client, async_session, usuario_teste):

    response = client.get(f'/usuarios/{usuario_teste.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário inexistente'}


@pytest.mark.asyncio
async def test_filial_vinculada_usuario_inexistente(
    client, async_session, empresa_teste, filial_teste
):

    await async_session.refresh(empresa_teste)
    await async_session.refresh(filial_teste)

    response = client.post(
        '/usuarios',
        json={
            'nome': 'teste',
            'email': 'teste@example.com',
            'senha': 'teste123',
            'empresa_id': empresa_teste.id,
            'filial_id': filial_teste.id + 1,
            'perfil': 'TESTE',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Filial inexistente'}


@pytest.mark.asyncio
async def test_usuario_empresa_inexistente(
    client, async_session, empresa_teste, usuario_teste, filial_teste
):

    await async_session.refresh(empresa_teste)
    await async_session.refresh(usuario_teste)

    response = client.get('/usuarios', params={'empresa_id': empresa_teste.id + 1})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Não existem usuários para esta empresa'}


@pytest.mark.asyncio
async def test_usuario_nao_vinculado_a_empresa(
    client, async_session, empresa_teste, usuario_teste, filial_teste
):

    await async_session.refresh(empresa_teste)
    await async_session.refresh(usuario_teste)

    response = client.get('/usuarios', params={'empresa_id': empresa_teste.id + 1})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Não existem usuários para esta empresa'}


@pytest.mark.asyncio
async def test_usuario_email_duplicado(client, usuario_teste, async_session):

    response = client.post(
        '/usuarios',
        json={
            'nome': 'teste',
            'email': usuario_teste.email,
            'senha': 'teste123',
            'empresa_id': usuario_teste.empresa_id,
            'filial_id': usuario_teste.filial_id,
            'perfil': 'TESTE',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email já cadastrado'}


@pytest.mark.asyncio
async def test_update_usuario_email_duplicado(
    client, usuario_teste, async_session, empresa_teste, filial_teste
):

    await async_session.refresh(usuario_teste)

    user = client.post(
        '/usuarios',
        json={
            'nome': 'teste',
            'email': 'teste_user@example.com',
            'senha': 'teste123',
            'empresa_id': usuario_teste.empresa_id,
            'filial_id': usuario_teste.filial_id,
            'perfil': 'TESTE',
        },
    )

    await async_session.refresh(usuario_teste)

    dados = {'email': usuario_teste.email}

    response = client.patch(f'/usuarios/{user.json()["id"]}', json=dados)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email já cadastrado'}
