from re import M

from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference, Theme
from models import categorias
from routers import (
    carrinho,
    catalogos,
    categorias,
    empresas,
    filiais,
    pedidos,
    produtos,
    usuarios,
)

app = FastAPI(title="Pede AI")


add_scalar_reference(
    app,
    route='/scalar',
    theme=Theme.DEEP_SPACE

)

app.include_router(empresas.router)
app.include_router(filiais.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(catalogos.router)
app.include_router(carrinho.router)
app.include_router(pedidos.router)
