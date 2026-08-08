from fastapi import FastAPI

from routers import empresas, filiais, usuarios

app = FastAPI()

app.include_router(empresas.router)
app.include_router(filiais.router)
app.include_router(usuarios.router)