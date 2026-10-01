from decimal import Decimal
from http import HTTPStatus
from re import sub

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import async_get_session   
from models.pedidos import PedidoItens, Pedidos, PedidoStatusHistorico
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


router = APIRouter(prefix='/pedido', tags=['Pedido'])

@router.post('/', response_model=s_pedido_response, status_code=HTTPStatus.CREATED)
async def criar_pedido(dado_carrinho_id: s_Pedido_Create, session=Depends(async_get_session)):

    """
    Cria um novo pedido com base no carrinho de compras fornecido.
    """


    carrinho = await session.scalar(select(Carrinho).where(Carrinho.id == dado_carrinho_id.carrinho_id)) #verifica se o carrinho existe no banco de dados

    if carrinho is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail="Carrinho não encontrado. Verifique se o carrinho existe.",
        )

    pedido_existente = await session.scalar(select(Pedidos).where(Pedidos.carrinho_id == dado_carrinho_id.carrinho_id))

    if pedido_existente:
        raise HTTPException(
            HTTPStatus.CONFLICT,
            detail=f'Já existe um pedido para este carrinho. PEDIDO Nº: {pedido_existente.id}'
        )
    filial = await session.scalar(select(Filiais).where(Filiais.id == carrinho.filial_id))
        

    carrinho_itens = (await session.scalars(select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho.id))).all()
    

    if not carrinho_itens:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail="Carrinho vazio, adicione um produto no carrinho"
        )



    objeto_produto = (
        await session.scalars(
            select(Produtos).where(
                Produtos.id.in_(
                    [item.produto_id for item in carrinho_itens]
                )
            )
        )
    ).all()


    pedido = Pedidos(

        carrinho_id = carrinho.id,
        empresa_id = filial.empresa_id,
        filial_id = filial.id,
        usuario_id = carrinho.usuario_id,
        status = Status_Pedidos.PENDENTE,
        previsao_entrega = None,
        entregue_em = None

    )


    lista_pedido_itens = []
    vt: list[Decimal] = []

    try:
        session.add(pedido)
        await session.flush()

        for item in carrinho_itens: 
            for produto in objeto_produto: #percorre a lista de produtos obtida do banco de dados e compara com os itens do carrinho para calcular o subtotal e criar os objetos relacionados ao pedido
                if item.produto_id == produto.id:
                    sub_total = item.quantidade * produto.preco
                    vt.append(sub_total)

                    pedido_itens = PedidoItens(
                        pedido_id=pedido.id,
                        produto_id=produto.id,
                        nome_produto=produto.nome,
                        preco_unitario=produto.preco,
                        quantidade=item.quantidade
                    ) #cria um objeto do tipo PedidoItens para cada item do carrinho, associando-o ao pedido recém-criado e armazenando informações sobre o produto, preço unitário e quantidade

                    pedidos_itens_l = s_Pedido_Out(
                            id_produto=produto.id,
                            nome=produto.nome,
                            quantidade=item.quantidade,
                            sub_total=sub_total) # cria um objeto do tipo s_Pedido_Out para cada item do pedido, contendo informações sobre o produto, quantidade e subtotal

                    lista_pedido_itens.append(pedidos_itens_l)  
                    session.add(pedido_itens)
        
        pedido_historico = PedidoStatusHistorico(
            pedido_id=pedido.id,
            status=Status_Pedidos.PENDENTE,
            alterado_por=pedido.usuario_id,
        ) #crie historico no pedido, para saber quem alterou o status do pedido e quando foi alterado

        pedido_response = s_pedido_response(
            id_pedido=pedido.id,
            empresa_id=pedido.empresa_id,
            filial_id=pedido.filial_id,
            usuario_id=pedido.usuario_id,
            status=pedido.status,
            created_at=pedido.created_at,
            valor_total=sum(vt, Decimal(0)),
            itens=lista_pedido_itens
        ) ## devolve no swagger


        session.add(pedido_historico)


        for item in carrinho_itens:
            await session.delete(item)

        await session.commit()

    except IntegrityError as e:

        await session.rollback()
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR,
                             detail="Erro ao criar o pedido. Verifique os dados fornecidos.")

    return pedido_response


@router.get('/{id_pedido}/', status_code=HTTPStatus.OK,response_model=s_pedido_response)
async def ler_pedido(id_pedido: int, session=Depends(async_get_session)):

    pedido = await session.scalar(select(Pedidos).where(Pedidos.id == id_pedido))

    sub_totais = []
    pedido_itens_lista = []


    if pedido is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Pedido inexistente'
        )

    pedidos_itens_scalar_result = await session.scalars(
        select(PedidoItens).where(PedidoItens.pedido_id == pedido.id))

    pedido_itens_all = pedidos_itens_scalar_result.all()
    for item in pedido_itens_all:

        item_out = s_Pedido_Out(
            id_produto=item.produto_id,
            nome=item.nome_produto,
            quantidade=item.quantidade,
            sub_total=item.preco_unitario * item.quantidade
        )

        pedido_itens_lista.append(item_out)
        sub_totais.append(item.preco_unitario * item.quantidade)

    

    pedido_response = s_pedido_response(

            id_pedido=pedido.id,
            empresa_id=pedido.empresa_id,
            filial_id=pedido.filial_id,
            usuario_id=pedido.usuario_id,
            status=pedido.status,
            created_at=pedido.created_at,
            valor_total=sum(sub_totais, Decimal(0)),
            itens=pedido_itens_lista
    )        

    return pedido_response


@router.patch('/{id_pedido}/status', status_code=HTTPStatus.OK):
def atualizar_status_pedido(id_pedido: int, status_update: s_Pedido_Update_create_status, session=Depends(async_get_session)):

    pedido = session.scalar(select(Pedidos).where(Pedidos.id == id_pedido))

    if pedido is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Pedido inexistente'
        )

    
    
    return {"message": "Status do pedido atualizado com sucesso."}