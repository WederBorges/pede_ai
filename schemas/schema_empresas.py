from datetime import datetime

from pydantic import BaseModel, ConfigDict


class s_Empresas_create(BaseModel):
    nome: str
    centro_de_custo: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class s_Empresas_out(BaseModel):
    id: int
    nome: str
    centro_de_custo: int
    created_at: datetime
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class s_Empresas_response(BaseModel):
    empresas: list[s_Empresas_out]  
