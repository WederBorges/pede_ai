from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.sessions import async_get_session

from models.produtos import Produtos
from schemas.schema_utils import Message
from schemas.schema_produtos import (
    s_Produtos_create,
    s_Produtos_out,
    s_Produtos_response,
    s_Produtos_update,
    s_Produtos_update_out,
)

router = APIRouter(prefix='/produtos')

router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Produtos_out)
async def create_produto(produto: s_Produtos_create, session=Depends(async_get_session)):

    stmt = select(Produtos).where(Produtos.nome == produto.nome)
    produto_existente = await session.scalar(stmt)

    if produto_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Produto já existe'
        )

    db_produto = Produtos(**produto.model_dump(exclude_unset=True))

    try:
        session.add(db_produto)
        await session.commit()
        await session.refresh(db_produto)
        return db_produto
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Erro ao criar produto: {str(e)}'
        )

router.get('/', response_model=list[s_Produtos_out])
async def ler_produtos(session=Depends(async_get_session)):

    produtos = await session.scalars(select(Produtos))

    if produtos is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nenhum produto encontrado'
        )

    return {'produtos': produtos.all()}