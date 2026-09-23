from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.pedidos import Pedidos
from models.empresas_e_filiais import Empresas, Filiais
from models.carrinho import Carrinho, CarrinhoItens
from schemas.schema_pedidos import (
    s_Pedido_Create,
    s_Pedido_Out,
    s_pedido_response,
    s_Pedido_Update_create_status,
    s_Pedido_Update_create_preventrega,
)


from schemas.schema_utils import Message
router = APIRouter(prefix='/pedido', tags=['Pedido'])

@router.post('/', response_model=s_pedido_response, status_code=HTTPStatus.CREATED)
async def criar_pedido(dado_carrinho_id: s_Pedido_Create, session=Depends(async_get_session)):

    """
    Cria um novo pedido com base no carrinho de compras fornecido.
    """


    carrinho = await session.scalar(select(Carrinho).where(Carrinho.id == dado_carrinho_id.carrinho_id))
    carrinho_itens = await session.scalars(select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho.id))
 

    pedido_existente = await session.scalar(select(Pedidos).where(Pedidos.carrinho_id == dado_carrinho_id.carrinho_id))

    if carrinho is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Carrinho não encontrado. Verifique se o carrinho existe.",
        )

    if pedido_existente:
        return pedido_existente  # Retorna o pedido existente se já houver um para o carrinho fornecido


    filiail = await session.scalar(select(Filiais).where(Filiais.id == carrinho.filial_id))
    
    pedido = Pedidos(    
            carrinho_id = carrinho.id,
            empresa_id = filiail.empresa_id,
            filial_id = filiail.id,
            usuario_id = carrinho.usuario_id
    )
    

    try:
        session.add(pedido)
        await session.commit()
        await session.refresh(pedido)

        pedido_criado = {

            "id_pedido": pedido.id,
            "empresa_id": pedido.empresa_id,
            "filial_id": pedido.filial_id,
            "usuario_id": pedido.usuario_id,
            "status": pedido.status,
            "created_at": pedido.created_at,
            "valor_total": sum(item.sub_total for item in carrinho_itens),
            "itens": [
                s_Pedido_Out(
                    id_produto=item.produto_id,
                    nome=item.produto.nome,
                    quantidade=item.quantidade,
                    sub_total=item.sub_total
                )
                for item in carrinho_itens
            ]
        }


        return pedido_criado

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Erro ao criar o pedido. Verifique se o" \
            " carrinho existe e se não há pedidos duplicados.")
