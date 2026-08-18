from pydantic import BaseModel, ConfigDict


class s_Categorias_create(BaseModel):
    nome: str
    descricao: str | None = None
    ativo: bool | None = True

    model_config = ConfigDict(from_attributes=True)


class s_Categorias_out(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    ativo: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class s_Categorias_response(BaseModel):
    categorias: list[s_Categorias_out]

    model_config = ConfigDict(from_attributes=True)


class s_Categorias_update(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    ativo: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class s_Categorias_update_out(BaseModel):
    id: int
    nome: str
    descricao: str
    ativo: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)
