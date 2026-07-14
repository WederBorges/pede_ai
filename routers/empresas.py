from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from db.sessions import async_get_session
from models.empresas import Empresas
from schemas.schema_empresas import (
    s_Empresas_create,
    s_Empresas_out,
    s_Empresas_response,
)

router = APIRouter(prefix='/empresas')


@router.get('/', status_code=200, response_model=s_Empresas_response)
async def ler_empresas(session=Depends(async_get_session)):

    empresas = await session.scalars(select(Empresas))

    return {'empresas': empresas.all()}


@router.get('/{id_user}', status_code=HTTPStatus.OK, response_model=s_Empresas_out)
async def ler_empresa_unica(id_user: int, session=Depends(async_get_session)):

    stmt = select(Empresas).where(Empresas.id == id_user)
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
