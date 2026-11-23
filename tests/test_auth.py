from http import HTTPStatus

from models.enums_perfil import Perfis
import pytest

permissoes_perfis = [
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
]

@pytest.mark.parametrize(
    ('perfil_usu_atual', 'perfil_requisitado', 'resposta_http'),
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
    indirect=['perfil_usu_atual'],
)