from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.categorias import Categoria
from schemas.schema_utils import Message

from schemas.schema_categorias import (
    s_Categorias_create,
    s_Categorias_out,
    s_Categorias_response,
    s_Categorias_update,
    s_Categorias_update_out,
)

router = APIRouter(prefix='/categorias')

@router.get('/', status_code=HTTPStatus.OK ,response_model=s_Categorias_response)
async def ler_categorias(session=Depends(async_get_session)):

    categorias = await session.scalars(select(Categoria))

    if categorias is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nenhuma categoria encontrada'
        )

    return {'categorias': categorias.all()}

@router.get('/{id_categoria}', status_code=HTTPStatus.OK, response_model=s_Categorias_out)
async def ler_categoria_unica(id_categoria: int, session=Depends(async_get_session)):
    
    stmt = select(Categoria).where(Categoria.id == id_categoria)
    categoria = await session.scalar(stmt)

    if categoria:
        return categoria

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada'
    )

@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Categorias_out)
async def criar_categoria(categoria: s_Categorias_create, session=Depends(async_get_session)):

    stmt = select(Categoria).where(Categoria.nome == categoria.nome)
    categoria_existente = await session.scalar(stmt)

    if categoria_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Categoria já existe'
        )

    db_categoria = Categoria(**categoria.model_dump(exclude_unset=True))

    try:
        session.add(db_categoria)
        await session.commit()
        await session.refresh(db_categoria)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao criar categoria'
        )
    return db_categoria


@router.patch('/{id_categoria}', status_code=HTTPStatus.OK, response_model=s_Categorias_update_out)
async def atualizar_categoria(id_categoria: int, categoria: s_Categorias_update, session=Depends(async_get_session)):

    stmt = select(Categoria).where(Categoria.id == id_categoria)
    db_categoria = await session.scalar(stmt)

    if not db_categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada'
        )

    if  categoria.nome is not None and db_categoria.nome != categoria.nome:
        stmt = select(Categoria).where(Categoria.nome == categoria.nome)
        categoria_existente = await session.scalar(stmt)

        if categoria_existente:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Categoria já existe'
            )

    for key, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_categoria, key, value)

    try:
        await session.commit()
        await session.refresh(db_categoria)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao atualizar categoria'
        )

    return db_categoria

@router.delete('/{id_categoria}', status_code=HTTPStatus.OK, response_model=Message)
async def deletar_categoria(id_categoria: int, session=Depends(async_get_session)):

    stmt = select(Categoria).where(Categoria.id == id_categoria)
    db_categoria = await session.scalar(stmt)

    if not db_categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada'
        )

    try:
        await session.delete(db_categoria)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao deletar categoria'
        )

    return {'message': 'Categoria deletada com sucesso'}