from http import HTTPStatus
from tkinter import NO

from models.enums_perfil import Perfis
import pytest
from models.usuarios import User
from sqlalchemy import select

@pytest.mark.parametrize(
    ('client', 'perfil_requisitado', 'http_esperado'),
    [
        # Usuário chave
        (Perfis.USUARIO_CHAVE, Perfis.USUARIO_CHAVE, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_CHAVE, Perfis.USUARIO_APOIO, HTTPStatus.CREATED),
        (Perfis.USUARIO_CHAVE, Perfis.USUARIO_CORPORATIVO, HTTPStatus.CREATED),
        (Perfis.USUARIO_CHAVE, Perfis.USUARIO_FILIAL, HTTPStatus.CREATED),
        (Perfis.USUARIO_CHAVE, Perfis.OPERADOR, HTTPStatus.CREATED),

        # Usuário apoio
        (Perfis.USUARIO_APOIO, Perfis.USUARIO_CHAVE, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_APOIO, Perfis.USUARIO_APOIO, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_APOIO, Perfis.USUARIO_CORPORATIVO, HTTPStatus.CREATED),
        (Perfis.USUARIO_APOIO, Perfis.USUARIO_FILIAL, HTTPStatus.CREATED),
        (Perfis.USUARIO_APOIO, Perfis.OPERADOR, HTTPStatus.CREATED),

        # Usuário corporativo não pode criar usuários
        (Perfis.USUARIO_CORPORATIVO, Perfis.USUARIO_CHAVE, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_CORPORATIVO, Perfis.USUARIO_APOIO, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_CORPORATIVO, Perfis.USUARIO_CORPORATIVO, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_CORPORATIVO, Perfis.USUARIO_FILIAL, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_CORPORATIVO, Perfis.OPERADOR, HTTPStatus.FORBIDDEN),

        # Usuário filial não pode criar usuários
        (Perfis.USUARIO_FILIAL, Perfis.USUARIO_CHAVE, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_FILIAL, Perfis.USUARIO_APOIO, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_FILIAL, Perfis.USUARIO_CORPORATIVO, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_FILIAL, Perfis.USUARIO_FILIAL, HTTPStatus.FORBIDDEN),
        (Perfis.USUARIO_FILIAL, Perfis.OPERADOR, HTTPStatus.FORBIDDEN),

        # Operador não pode criar usuários
        (Perfis.OPERADOR, Perfis.USUARIO_CHAVE, HTTPStatus.FORBIDDEN),
        (Perfis.OPERADOR, Perfis.USUARIO_APOIO, HTTPStatus.FORBIDDEN),
        (Perfis.OPERADOR, Perfis.USUARIO_CORPORATIVO, HTTPStatus.FORBIDDEN),
        (Perfis.OPERADOR, Perfis.USUARIO_FILIAL, HTTPStatus.FORBIDDEN),
        (Perfis.OPERADOR, Perfis.OPERADOR, HTTPStatus.FORBIDDEN),
    ],
    indirect=['client'],
)
@pytest.mark.asyncio
async def test_criar_user_perfis_diferentes(
    async_session,
    client,
    perfil_requisitado,
    http_esperado,
    empresa_teste,
    filial_teste
):

    dados = {
        'nome': 'usuario_teste',
        'email': 'test_email@xample.com.br',
        'perfil': perfil_requisitado.value,
        'senha': 'senha_example',
        'empresa_id': empresa_teste.id,
        'filial_id': filial_teste.id
    }

    response = client.post('/usuarios', json=dados)

    assert response.status_code == http_esperado, response.json()

    if response.status_code == HTTPStatus.CREATED:
        stmt = select(User).where(User.id == response.json()['id'])
        user = await async_session.scalar(stmt)
        assert user is not None
        assert perfil_requisitado == user.perfil

    elif response.status_code == HTTPStatus.FORBIDDEN:
        stmt = select(User).where(User.email == dados['email'])
        user = await async_session.scalar(stmt)
        assert user is None
