from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.carrinho import Carrinho, CarrinhoItens
from models.usuarios import User
from models.empresas_e_filiais import Filiais
from models.produtos import Produtos
from schemas.schema_utils import Message
from schemas.schema_carrinho import(
     
s_Produto_Input_carrinho, 
s_Produto_Output_carrinho, 
s_Create_carrinho, 
s_Create_carrinho_out, 
s_Produtos_response_carrinho

)

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

@router.post('/{id_carrinho}/produtos', response_model=s_Produtos_response_carrinho)
async def adicionar_produto_carrinho(
    id_carrinho: int,
    produto_entrada: s_Produto_Input_carrinho,
    session=Depends(async_get_session)
):


    carrinho = await session.scalar(select(Carrinho).where(Carrinho.id == id_carrinho))
    produto = await session.scalar(select(Produtos).where(Produtos.id == produto_entrada.produto_id))

    if carrinho is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Carrinho inexistente')
    if produto is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Produto inexistente')

    carrinho_e_produto = await session.scalar(
        select(CarrinhoItens).where(
                CarrinhoItens.carrinho_id == id_carrinho,
                CarrinhoItens.produto_id == produto_entrada.produto_id
            )
        )


    if carrinho_e_produto is None:
        try:
            carrinho_item = CarrinhoItens(
                carrinho_id=id_carrinho,
                produto_id=produto_entrada.produto_id,
                quantidade=produto_entrada.quantidade
            )
            session.add(carrinho_item)
            await session.commit()
            await session.refresh(carrinho_item)

            item_montado = {
                'id': carrinho_item.id,
                'categoria_id': produto.categoria_id,
                'nome': produto.nome,
                'preco': produto.preco,
                'quantidade': carrinho_item.quantidade,
                'preco_total': carrinho_item.quantidade * produto.preco,
                'imagem_url': produto.imagem_url,
                }

            return {'produtos_carrinho': [item_montado]}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao adicionar produto ao carrinho')

    else:
        carrinho_e_produto.quantidade += produto_entrada.quantidade
        try:
            await session.commit()
            await session.refresh(carrinho_e_produto)

            item_montado = {
                'id': carrinho_e_produto.id,
                'categoria_id': produto.categoria_id,
                'nome': produto.nome,
                'preco': produto.preco,
                'quantidade': carrinho_e_produto.quantidade,
                'preco_total': carrinho_e_produto.quantidade * produto.preco,
                'imagem_url': produto.imagem_url,
                }

            return {'produtos_carrinho': [item_montado]}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Erro ao atualizar quantidade do produto no carrinho')