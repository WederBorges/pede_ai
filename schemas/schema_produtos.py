
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from typing import Annotated

class s_Produtos_create(BaseModel):

    categoria_id: int
    nome: str
    descricao: str
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    imagem_url: str | None = None
    ativo: bool | None = True

    model_config = ConfigDict(from_attributes=True)

class s_Produtos_out(BaseModel):

    id: int
    categoria_id: int
    nome: str
    descricao: str
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    imagem_url: str | None = None
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class s_Produtos_response(BaseModel):

    produtos: list[s_Produtos_out]

    model_config = ConfigDict(from_attributes=True)

class s_Produtos_update(BaseModel):

    categoria_id: int | None = None
    nome: str | None = None
    descricao: str | None = None
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)] | None = None
    imagem_url: str | None = None
    ativo: bool | None = None

    model_config = ConfigDict(from_attributes=True)

class s_Produtos_update_out (BaseModel):

    id: int
    categoria_id: int
    nome: str
    descricao: str
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    imagem_url: str | None = None
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)