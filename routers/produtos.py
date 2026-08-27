from operator import and_

from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.sessions import async_get_session

from models.produtos import Produtos
from models.categorias import Categoria
from schemas.schema_utils import Message
from schemas.schema_produtos import (
    s_Produtos_create,
    s_Produtos_out,
    s_Produtos_response,
    s_Produtos_update,
    s_Produtos_update_out,
)

router = APIRouter(prefix='/produtos')

@router.post('/', status_code=HTTPStatus.CREATED, response_model=s_Produtos_out)
async def create_produto(produto: s_Produtos_create, session=Depends(async_get_session)):

    stmt = select(Produtos).where(Produtos.nome == produto.nome)
    produto_existente = await session.scalar(stmt)

    if produto_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Produto já existe'
        )

    stmt2 = select(Categoria).where(Categoria.id == produto.categoria_id)
    categoria_existente = await session.scalar(stmt2)

    if categoria_existente is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria inexistente'
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

@router.get('/', status_code=HTTPStatus.OK, response_model=s_Produtos_response)
async def ler_produtos(session=Depends(async_get_session)):
    produtos = await session.scalars(select(Produtos))
    return {'produtos': produtos.all()}


@router.delete('/{id_produto}', status_code=HTTPStatus.OK ,response_model=Message)
async def apagar_produto(id_produto ,session=Depends(async_get_session)):

    stmt = select(Produtos).where(Produtos.id == id_produto)
    produto_existe = await session.scalar(stmt)

    if produto_existe is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Produto inexistente'
        )

    await session.delete(produto_existe)
    await session.commit()
    return {'message':'Produto excluído'}

@router.patch('/{id_produto}', status_code=HTTPStatus.OK, response_model=s_Produtos_update_out)
async def atualizar_produto(id_produto ,dados: s_Produtos_update, session=Depends(async_get_session)):

    produto = await session.scalar(select(Produtos).where(Produtos.id == id_produto))
    
    if produto is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Produto inexistente'
        )

    if dados.nome != produto.nome:
        stmt = select(Produtos).where(
            Produtos.nome == dados.nome,
        )
        
        produto_divergente = await session.scalar(stmt)
        if produto_divergente is not None:
                raise HTTPException(
                    HTTPStatus.CONFLICT,
                    detail='Produto já cadastrado'
                )
        
    
    if dados.categoria_id is None:
        categoria = await session.scalar(select(Categoria).where(Categoria.id == produto.categoria_id))
        dados.categoria_id = categoria.id
        if categoria is None:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail='Produto inexistente'
            )

    db_produto = dados.model_dump(exclude_unset=True)

    for key, value in db_produto.items():
        setattr(produto, key, value)

    try:
        await session.commit()
        await session.refresh(produto)
        return produto
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            HTTPStatus.CONFLICT
        )

