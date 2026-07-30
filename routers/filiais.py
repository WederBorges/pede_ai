from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.empresas_e_filiais import Filiais, Empresas
from schemas.schema_empresas import s_Empresas_out
from schemas.schema_filiais import (
    s_Filiais_create,
    s_Filiais_out,
    s_Filiais_response,
    s_Filiais_update,
    s_Filiais_update_out,
)

router = APIRouter(prefix='/filiais')

@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Filiais_out)
async def create_filial(
    dados: s_Filiais_create, session=Depends(async_get_session)):
    
    stmt = select(Empresas).where(Empresas.id == dados.empresa_id) 
    empresa = await session.scalar(stmt)

    if not empresa:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail="Associação a uma empresa inexistente"
        )

    filial = Filiais(

        nome = dados.nome,
        empresa_id = dados.empresa_id,
        cidade = dados.cidade,
        estado = dados.estado,
        ativo = dados.ativo
    )
    
    session.add(filial)
    await session.commit()
    await session.refresh(filial)
    return filial