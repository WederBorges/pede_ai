from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from models.enums_pedido import Status_Pedidos


class s_Pedido_Create(BaseModel):
    carrinho_id: int

    model_config = ConfigDict(from_attributes=True)


class s_Pedido_Update_create_status(BaseModel):
    status: Status_Pedidos

    model_config = ConfigDict(from_attributes=True)


class s_Pedido_Update_create_preventrega(BaseModel):
    previsao_entrega: date

    model_config = ConfigDict(from_attributes=True)


# schema de resposta


class s_Pedido_Out(BaseModel):
    id_produto: int
    nome: str
    quantidade: int
    sub_total: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

    model_config = ConfigDict(from_attributes=True)


class s_pedido_response(BaseModel):
    id_pedido: int
    empresa_id: int
    filial_id: int
    usuario_id: int
    status: Status_Pedidos
    created_at: datetime
    previsao_entrega: date | None
    valor_total: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    itens: list[s_Pedido_Out]

    model_config = ConfigDict(from_attributes=True)
