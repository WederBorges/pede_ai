from fastapi import FastAPI

from routers import empresas


app = FastAPI()

app.include_router(empresas.router)