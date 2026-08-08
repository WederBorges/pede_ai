from http import HTTPStatus
from uuid import RESERVED_FUTURE

from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import QueryParams
from sqlalchemy import select
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.usuarios import User
from schemas.schemas_usuario import (
    s_Usuario_created,
    s_Usuario_out,
    s_Usuarios_Response
)
from schemas.schema_utils import Message

router = APIRouter(prefix='/usuarios')


@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Usuario_out)
async def create_user(dados: s_Usuario_created, session=Depends(async_get_session)):

    model = User(
        nome = dados.nome,
        email = dados.email,
        perfil = dados.perfil,
        senha_hash = dados.senha,
        empresa_id = dados.empresa_id,
        filial_id = dados.filial_id,
        
    )
    
    try:
        session.add(model)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            HTTPStatus.CONFLICT
        )

    await session.refresh(model)
    return model

@router.get('/', status_code=HTTPStatus.OK, response_model=s_Usuarios_Response)
async def read_all_users(id_empresa:int | None = None ,session = Depends(async_get_session)): 

    if id_empresa:
        stmt = select(User).where(User.empresa_id == id_empresa)
        all_users = await session.scalars(stmt)

        if not all_users.all():
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail='Não existem usuários para esta empresa'
            )
        return {'usuarios': all_users.all()}        

    stmt = select(User)
    all_users = await session.scalars(stmt)
    
    return {'usuarios': all_users.all()}