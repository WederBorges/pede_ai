from datetime import datetime

from pydantic import BaseModel, ConfigDict


class s_Filiais_create(BaseModel):
    nome: str
    empresa_id: int
    cidade: str
    estado: str
    ativo: bool = False

    model_config = ConfigDict(from_attributes=True)


class s_Filiais_out(BaseModel):
    id: int
    nome: str
    empresa_id: int
    cidade: str
    estado: str
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class s_Filiais_update(BaseModel):
    nome: str | None = None
    empresa_id: int | None = None
    cidade: str | None = None
    estado: str | None = None
    ativo: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class s_Filiais_update_out(BaseModel):
    id: int
    nome: str
    empresa_id: int
    cidade: str
    estado: str
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class s_Filiais_response(BaseModel):
    filiais: list[s_Filiais_out]
