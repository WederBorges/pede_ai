from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.empresas import Empresas
from schemas.schema_empresas import (
    s_Empresas_create,
    s_Empresas_out,
    s_Empresas_response,
    s_Empresas_update,
    s_Empresas_update_out,
)

router = APIRouter(prefix='/empresas')


@router.get('/', status_code=200, response_model=s_Empresas_response)
async def ler_empresas(session=Depends(async_get_session)):

    empresas = await session.scalars(select(Empresas))

    return {'empresas': empresas.all()}


@router.get(
    '/{id_empresa}', status_code=HTTPStatus.OK, response_model=s_Empresas_create
)
async def ler_empresa_unica(id_empresa: int, session=Depends(async_get_session)):

    stmt = select(Empresas).where(Empresas.id == id_empresa)
    empresa = await session.scalar(stmt)

    if empresa:
        return empresa

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Empresa não encontrada'
    )


@router.post('/', status_code=201, response_model=s_Empresas_out)
async def inputar_empresas(
    dados: s_Empresas_create,
    session=Depends(async_get_session),
):
    empresa = Empresas(
        nome=dados.nome, centro_de_custo=dados.centro_de_custo, ativo=dados.ativo
    )

    session.add(empresa)
    await session.commit()
    await session.refresh(empresa)
    return empresa


@router.delete('/{id_empresa}', status_code=HTTPStatus.NO_CONTENT)
async def delete_empresa(id_empresa: int, session=Depends(async_get_session)):

    stmt = select(Empresas).where(Empresas.id == id_empresa)
    empresa = await session.scalar(stmt)

    if not empresa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Empresa inexistente'
        )

    await session.delete(empresa)
    await session.commit()


@router.patch(
    '/{id_empresa}', status_code=HTTPStatus.OK, response_model=s_Empresas_update_out
)
async def update_empresa(
    id_empresa: int, dados: s_Empresas_update, session=Depends(async_get_session)
):

    stmt = select(Empresas).where(Empresas.id == id_empresa)
    empresa = await session.scalar(stmt)

    if not empresa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Empresa inexistente'
        )

    try:
        dados_exclude_none = dados.model_dump(
            exclude_unset=True
        )  # Exclui dados == None

        for (
            k,
            v,
        ) in dados_exclude_none.items():  # Seta apenas os dados existentes no objeto.
            setattr(empresa, k, v)

        await session.commit()
        await session.refresh(empresa)
        return empresa

    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT)
