from fastapi import FastAPI
from fastapi import Depends

from starlette.status import HTTP_201_CREATED
from db.sessions import async_get_session
from typing import Any

from models.empresas import Empresas
from schemas.schema_empresas import s_Empresas_out, s_Empresas_create, s_Empresas_response
from sqlalchemy import select


app = FastAPI()

@app.get('/')
def read_root():
    return {"hello": "word"}

@app.get('/empresas', status_code=200, response_model=s_Empresas_response)
async def empresas(session = Depends(async_get_session)):
    
    empresas = await session.scalars(select(Empresas))

    return  {
        'empresas':empresas.all()
    }

@app.post('/', status_code=201 ,response_model=s_Empresas_out)
async def inputar_empresas(
    dados: s_Empresas_create,
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