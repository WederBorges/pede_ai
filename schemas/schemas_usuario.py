from pydantic import BaseModel, ConfigDict
from datetime import datetime

# d
# empresa_id
# filial_id
# nome
# email
# senha_hash
# perfil
# created_at
class s_Usuario_created(BaseModel):

    nome: str
    email: str
    perfil: str
    senha: str
    empresa_id: int
    filial_id: int|None = None

    model_config = ConfigDict(from_attributes=True)

class s_Usuario_out(BaseModel):

    id: int
    nome: str
    email: str
    perfil: str
    empresa_id: int
    filial_id: int|None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class s_Usuarios_Response(BaseModel):

    usuarios: list[s_Usuario_out]