from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.carrinho import Carrinho
from models.usuarios import User
from models.empresas_e_filiais import Filiais
from schemas.schema_utils import Message
from schemas.schema_carrinho import s_Produto_Output_carrinho, s_Create_carrinho, s_Create_carrinho_out, s_Produtos_response_carrinho

router = APIRouter(prefix='/carrinho')

@router.post('/', response_model=s_Create_carrinho_out)
async def criar_carrinho(
    dados: s_Create_carrinho,
    response: Response, 
    session=Depends(async_get_session)):

    filial = await session.scalar(select(Filiais).where(Filiais.id == dados.filial_id))
    usuario = await session.scalar(select(User).where(User.id == dados.usuario_id))

    if filial is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Filial inexistente')

    if usuario is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Usuário inexistente')

    carrinho = await session.scalar(select(Carrinho).where(Carrinho.usuario_id == usuario.id ))

    if carrinho is None:
        carrinho = Carrinho(**dados.model_dump())
        
        try:
            session.add(carrinho)
            await session.commit()
            await session.refresh(carrinho)
            response.status_code = HTTPStatus.CREATED
            return carrinho
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao criar carrinho')

    response.status_code = HTTPStatus.OK
    return carrinho