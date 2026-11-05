# Validação rota usuarios ####
from decimal import Decimal
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from models import pedidos
from models.empresas_e_filiais import Empresas, Filiais
from routers import pedidos
from models.pedidos import PedidoItens, Pedidos
from schemas.schema_pedidos import s_Pedido_Out, s_pedido_response
from sqlalchemy.ext.asyncio import AsyncSession

async def montar_resumo_pedido(session: AsyncSession, pedido: Pedidos) -> s_pedido_response:
    """
    Função para montar o resumo de um pedido.
    
    """    
    
    sub_totais = []
    pedido_itens_lista = []
    
    itens_do_pedido = await session.scalars(
        select(PedidoItens).where(PedidoItens.pedido_id == pedido.id)
    )
    itens_do_pedido_all = itens_do_pedido.all()
    
    ##### 1 - Montar s_pedido_out ######
    
    for item in itens_do_pedido_all:
        item_pedido_out = s_Pedido_Out(
            id_produto=item.produto_id,
            nome=item.nome_produto,
            quantidade=item.quantidade,
            sub_total=item.preco_unitario * item.quantidade,
        )
        pedido_itens_lista.append(item_pedido_out)
        sub_totais.append(item.preco_unitario * item.quantidade)

    ##### 2 - Montar s_pedido_response ######
    
    pedido_response = s_pedido_response(
        id_pedido=pedido.id,
        empresa_id=pedido.empresa_id,
        filial_id=pedido.filial_id,
        usuario_id=pedido.usuario_id,
        status=pedido.status,
        created_at=pedido.created_at,
        previsao_entrega=pedido.previsao_entrega,
        valor_total=sum(sub_totais, Decimal(0)),
        itens=pedido_itens_lista,
    )



    return pedido_response
