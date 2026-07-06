from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from datetime import datetime
from models.empresas import Empresas
from pede_ai.db.sessions import async_get_session
from typing import Any

app = FastAPI()


class Empresas_update(BaseModel):
    id: str
    nome: str
    centro_de_custo: str
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

@app.put('/')
async def inputar_empresas(
    dados: Empresas_update,
    session = Depends(async_get_session)
):
   session.add()