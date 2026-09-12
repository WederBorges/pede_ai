from fastapi import FastAPI

from models import categorias
from routers import (
    carrinho,
    catalogos,
    categorias,
    empresas,
    filiais,
    produtos,
    usuarios,
)

app = FastAPI()

app.include_router(empresas.router)
app.include_router(filiais.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(catalogos.router)
app.include_router(carrinho.router)
