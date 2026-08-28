from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from decimal import Decimal



class s_Catalogo_out(BaseModel):

    categoria_id: int
    nome: str 
    descricao: str | None 
    preco: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    imagem_url: str | None
    
    model_config = ConfigDict(from_attributes=True)

class s_Catalogo_response(BaseModel):
    produtos: list[s_Catalogo_out]