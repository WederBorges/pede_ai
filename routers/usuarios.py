from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.empresas_e_filiais import Empresas, Filiais
from models.usuarios import User
from schemas.schema_utils import Message
from schemas.schemas_usuario import (
    s_Usuario_created,
    s_Usuario_out,
    s_Usuario_update_,
    s_Usuario_Update_out,
    s_Usuarios_Response,
)

router = APIRouter(prefix='/usuarios')


@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Usuario_out)
async def create_user(dados: s_Usuario_created, session=Depends(async_get_session)):

    model = User(
        nome=dados.nome,
        email=dados.email,
        perfil=dados.perfil,
        senha_hash=dados.senha,
        empresa_id=dados.empresa_id,
        filial_id=dados.filial_id,
    )

    stmt1 = await session.scalar(
        select(Empresas).where(Empresas.id == dados.empresa_id)
    )
    if not stmt1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Empresa não encontrada')
    if dados.filial_id is not None:
        stmt2 = await session.scalar(
            select(Filiais).where(Filiais.id == dados.filial_id)
        )
        if not stmt2:
            raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial não encontrada')

    try:
        session.add(model)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT)

    await session.refresh(model)
    return model


@router.get('/', status_code=HTTPStatus.OK, response_model=s_Usuarios_Response)
async def read_all_users(
    id_empresa: int | None = None, session=Depends(async_get_session)
):

    if id_empresa:
        stmt = select(User).where(User.empresa_id == id_empresa)
        all_users = await session.scalars(stmt)

        if not all_users.all():
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail='Não existem usuários para esta empresa'
            )
        return {'usuarios': all_users.all()}

    stmt = select(User)
    all_users = await session.scalars(stmt)

    return {'usuarios': all_users.all()}


@router.get('/{id_user}', status_code=HTTPStatus.OK, response_model=s_Usuario_out)
async def read_user(id_user: int, session=Depends(async_get_session)):

    stmt = select(User).where(User.id == id_user)
    user = await session.scalar(stmt)

    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Usuário inexistente')
    return user


@router.patch(
    '/{id_user}', status_code=HTTPStatus.OK, response_model=s_Usuario_Update_out
)
async def update_user(
    id_user: int, dados: s_Usuario_update_, session=Depends(async_get_session)
):

    stmt = select(User).where(User.id == id_user)
    user = await session.scalar(stmt)

    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Usuário inexistente')

    try:
        model = dados.model_dump(exclude_unset=True)

        for k, v in model.items():
            setattr(user, k, v)
        await session.commit()
        await session.refresh(user)
        return user

    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT)


@router.delete('/{id_user}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(id_user: int, session=Depends(async_get_session)):

    stmt = select(User).where(User.id == id_user)
    user = await session.scalar(stmt)

    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Usuário inexistente')

    try:
        await session.delete(user)
        await session.commit()
        return {'message': 'Usuário excluído'}

    except IntegrityError:
        await session.rollback()
        raise HTTPException(HTTPStatus.CONFLICT)
