from datetime import datetime
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class s_Create_carrinho(BaseModel):

    filial_id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)

class s_Create_carrinho_out(BaseModel):

    id: int
    filial_id: int
    usuario_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class s_Produto_Output_carrinho(BaseModel):

    id: int
    categoria_id: int
    nome: str 
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    quantidade: int
    preco_total: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    imagem_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

class s_Produto_Input_carrinho(BaseModel):

    quantidade: int = Field(gt=0)
    produto_id: int


    model_config = ConfigDict(from_attributes=True)

class s_Produtos_response_carrinho(BaseModel):

    produtos_carrinho: list[s_Produto_Output_carrinho]

    model_config = ConfigDict(from_attributes=True)
    