from fastapi import FastAPI

from models import categorias
from routers import empresas, filiais, usuarios, categorias, produtos

app = FastAPI()

app.include_router(empresas.router)
app.include_router(filiais.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(produtos.router)