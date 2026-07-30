from fastapi import FastAPI

from routers import empresas, filiais

app = FastAPI()

app.include_router(empresas.router)
app.include_router(filiais.router)
