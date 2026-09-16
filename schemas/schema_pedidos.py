from pydantic import BaseModel
from models.enums_pedido import Status_Pedidos
from datetime import date

class s_Pedido_Create(BaseModel):
    carrinho_id: int

class s_Pedido_Update_create_status(BaseModel):
    status: Status_Pedidos

class s_Pedido_Update_create_preventrega(BaseModel):
    previsao_entrega: date