# Validação rota usuarios ####
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from models.empresas_e_filiais import Empresas, Filiais


async def validar_filial_e_empresas(
    session, dados, empresa_id_atual=None, filial_id_atual=None
):

    empresa_id = (
        dados.empresa_id if dados.empresa_id is not None else empresa_id_atual
    )  # rota patch
    filial_id = (
        dados.filial_id if dados.filial_id is not None else filial_id_atual
    )  # rota post (create_user)

    if empresa_id is not None:
        stmt = select(Empresas).where(Empresas.id == empresa_id)
        validacao = await session.scalar(stmt)

        if validacao is None:
            raise HTTPException(HTTPStatus.CONFLICT, detail='Empresa inexistente')

    if filial_id is not None:
        stmt = select(Filiais).where(Filiais.id == filial_id)
        validacao1 = await session.scalar(stmt)

        if validacao1 is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial inexistente')

        stmt2 = select(Filiais).where(
            Filiais.id == filial_id, Filiais.empresa_id == empresa_id
        )
        validacao2 = await session.scalar(stmt2)

        if validacao2 is None:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail='Filial não pertence a empresa'
            )

    return empresa_id, filial_id
