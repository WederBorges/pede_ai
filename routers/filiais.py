from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.empresas_e_filiais import Empresas, Filiais
from schemas.schema_filiais import (
    s_Filiais_create,
    s_Filiais_out,
    s_Filiais_response,
    s_Filiais_update,
    s_Filiais_update_out,
)
from schemas.schema_utils import Message

router = APIRouter(prefix='/filiais')


@router.get('/', status_code=HTTPStatus.OK, response_model=s_Filiais_response)
async def ler_filiais(session=Depends(async_get_session)):

    dados = await session.scalars(select(Filiais))
    filiais = dados.all()

    if not filiais:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Não há registros')

    return {'filiais': filiais}


@router.get('/{id_filial}', status_code=HTTPStatus.OK, response_model=s_Filiais_out)
async def ler_filial_unica(id_filial: int, session=Depends(async_get_session)):

    stmt = select(Filiais).where(Filiais.id == id_filial)
    filial = await session.scalar(stmt)

    if not filial:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial inexistente')

    return filial


@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Filiais_out)
async def create_filial(dados: s_Filiais_create, session=Depends(async_get_session)):

    stmt = select(Empresas).where(Empresas.id == dados.empresa_id)
    empresa = await session.scalar(stmt)

    if not empresa:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Associação a uma empresa inexistente'
        )

    try:
        filial = Filiais(
            nome=dados.nome,
            empresa_id=dados.empresa_id,
            cidade=dados.cidade,
            estado=dados.estado,
            ativo=dados.ativo,
        )

        session.add(filial)
        await session.commit()
        await session.refresh(filial)
        return filial

    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT, detail='Entrada de dados inválida')


@router.delete('/{id_filial}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_filial(id_filial: int, session=Depends(async_get_session)):

    stmt = select(Filiais).where(Filiais.id == id_filial)

    filial = await session.scalar(stmt)
    if not filial:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial inexistente')

    try:
        await session.delete(filial)
        await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT)
    return {'message': 'Filial excluída'}


@router.patch(
    '/{id_filial}', status_code=HTTPStatus.OK, response_model=s_Filiais_update_out
)
async def update_filiais(
    id_filial: int, dados: s_Filiais_update, session=Depends(async_get_session)
):

    stmt = select(Filiais).where(Filiais.id == id_filial)
    filial = await session.scalar(stmt)

    if not filial:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial inexistente')

    if dados.empresa_id is not None:
        stmt = select(Empresas).where(Empresas.id == dados.empresa_id)
        empresa = await session.scalar(stmt)
        if not empresa:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail='Empresa vinculada inexistente'
            )

    filial_clear_none = dados.model_dump(exclude_unset=True)

    try:
        for k, v in filial_clear_none.items():
            setattr(filial, k, v)

        await session.commit()
        await session.refresh(filial)

    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            HTTPStatus.CONFLICT,
            detail='Não é possível ter 2 filiais com'
            ' o mesmo nome para a mesma organização',
        )

    return filial
