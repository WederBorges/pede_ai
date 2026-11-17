from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from sqlalchemy import select
from models.usuarios import User
from schemas.schema_auth_ import s_create_auth ,s_create_auth_out
from fastapi import Depends
from db.sessions import async_get_session
from services.services_auth import autenticar_usuario, gerar_token_usuario, get_current_user


router = APIRouter(prefix='/auth', tags=["Autenticação"])

@router.post('/login', status_code=HTTPStatus.OK, response_model=s_create_auth_out)
async def login(dados: s_create_auth, session=Depends(async_get_session)):

    user = await autenticar_usuario(dados.email, dados.senha, session)

    token = gerar_token_usuario(
            user.id,
            user.perfil,
            user.email,
            user.empresa_id,
            user.filial_id
    )

    return {"access_token":token}


@router.get('/me', status_code=HTTPStatus.OK)
async def auth_me(cred=Depends(get_current_user)):
    return cred