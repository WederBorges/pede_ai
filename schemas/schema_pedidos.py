
from pydantic import BaseModel
from datetime import date
from datetime import datetime
from typing import Annotated 
from decimal import Decimal
from pydantic import Field
from models.enums_pedido import Status_Pedidos
class s_Pedido_Create(BaseModel):
    carrinho_id: int

class s_Pedido_Update_create_status(BaseModel):
    status: Status_Pedidos

class s_Pedido_Update_create_preventrega(BaseModel):
    previsao_entrega: date

#schema de resposta


class s_Pedido_Out(BaseModel):
    
    id_produto:int
    nome:str
    quantidade: int
    sub_total: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
        

class s_pedido_response(BaseModel):

    id_pedido: int
    empresa_id:int
    filial_id:int 
    usuario_id:int
    status:Status_Pedidos
    created_at: datetime
    valor_total:Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    itens: list[s_Pedido_Out]
