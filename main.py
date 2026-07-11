from fastapi import FastAPI
from fastapi import Depends

from starlette.status import HTTP_201_CREATED
from db.sessions import async_get_session
from typing import Any

from models.empresas import Empresas
from schemas.schema_empresas import s_Empresas_out, s_Empresas_create, s_Empresas_response
from sqlalchemy import select

from routers import empresas


app = FastAPI()

app.include_router(empresas.router)