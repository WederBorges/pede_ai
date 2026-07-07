from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from datetime import datetime

from starlette.status import HTTP_201_CREATED
from models.empresas import Empresas
from db.sessions import async_get_session
from typing import Any

app = FastAPI()


class Empresas_update(BaseModel):
    id: int
    nome: str
    centro_de_custo: int
    created_at: datetime
    ativo: bool



@app.get('/')
def read_root():
    return {"hello": "word"}

@app.get('/empresas')
def empresas():
    
    return  {
        'empresas':['a','b','c','d', 'f', 'g']
    }

@app.post('/', status_code=201 ,response_model=Empresas_update)
async def inputar_empresas(
    dados: Empresas_update,
    session = Depends(async_get_session),
    
):
   empresa = Empresas(

    nome = dados.nome,
    centro_de_custo = dados.centro_de_custo,
    ativo = dados.ativo
   )
   
   session.add(empresa)
   await session.commit()
   await session.refresh(empresa)
   return empresa