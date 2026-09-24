from http import HTTPStatus
from math import e

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session
from models.pedidos import PedidoItens, Pedidos
from models.enums_pedido import Status_Pedidos
from models.empresas_e_filiais import Empresas, Filiais
from models.carrinho import Carrinho, CarrinhoItens
from models.produtos import Produtos
from schemas.schema_pedidos import (
    s_Pedido_Create,
    s_Pedido_Out,
    s_pedido_response,
    s_Pedido_Update_create_status,
    s_Pedido_Update_create_preventrega,
)


from schemas.schema_utils import Message
from tests.conftest import produto_teste
router = APIRouter(prefix='/pedido', tags=['Pedido'])

@router.post('/', response_model=s_pedido_response, status_code=HTTPStatus.CREATED)
async def criar_pedido(dado_carrinho_id: s_Pedido_Create, session=Depends(async_get_session)):

    """
    Cria um novo pedido com base no carrinho de compras fornecido.
    """


    carrinho = await session.scalar(select(Carrinho).where(Carrinho.id == dado_carrinho_id.carrinho_id)) #verifica se o carrinho existe no banco de dados
    if carrinho is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Carrinho não encontrado. Verifique se o carrinho existe.",
        )

    pedido_existente = await session.scalar(select(Pedidos).where(Pedidos.carrinho_id == dado_carrinho_id.carrinho_id))

    if pedido_existente:
        return pedido_existente  # Retorna o pedido existente se já houver um para o carrinho fornecido

    filial = await session.scalar(select(Filiais).where(Filiais.id == carrinho.filial_id))
        

    carrinho_itens = await session.scalars(select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho.id)).all()
    
    
    objeto_produto = (
        await session.scalars(
            select(Produtos).where(
                Produtos.id.in_(
                    [item.produto_id for item in carrinho_itens]
                )
            )
        )
    ).all()

    vt = []

    
    pedido = Pedidos(

        carrinho_id = carrinho.id,
        empresa_id = filial.empresa_id,
        filial_id = filial.id,
        usuario_id = carrinho.usuario_id,
        status = Status_Pedidos.PENDENTE,
        previsao_entrega = None,
        entregue_em = None

    )





    try:
        session.add(pedido)
        await session.flush()



        for item in carrinho_itens:
            for produto in objeto_produto:
                if item.produto_id == produto.id:
                    sub_total = item.quantidade * produto.preco_unitario
                    vt.append(sub_total)

                    pedido_itens = PedidoItens(
                
                        pedido_id=pedido.id,
                        produto_id=produto.id,
                        nome_produto=produto.nome,
                        preco_unitario=produto.preco_unitario,
                        quantidade=item.quantidade


                    )
                    session.add(pedido_itens)
                    
        
        await session.commit()
    
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o pedido. Verifique os dados fornecidos.",
        )


