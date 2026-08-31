from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.categorias import Categoria
from models.produtos import Produtos
from schemas.schema_utils import Message

from schemas.schema_catalogo import (
    s_Catalogo_response,

)

router = APIRouter(prefix='/catalogo')


@router.get('/', status_code=HTTPStatus.OK ,response_model=s_Catalogo_response)
async def catalogo(
    categoria_id: int | None = None,
    produto: str | None = None,
    session=Depends(async_get_session)
):

    condicoes = [Produtos.ativo == True]
    if produto is not None:
        condicoes.append(Produtos.nome.ilike(f"%{produto}%"))
    if categoria_id is not None:
        condicoes.append(Produtos.categoria_id == categoria_id)
            

    stmt = select(Produtos).where(*condicoes)
    produtos = await session.scalars(stmt)
    return {'produtos': produtos.all()}
     