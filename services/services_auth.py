from ast import Try
from datetime import datetime, timedelta, timezone, tzinfo
from pydoc import doc
from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios import User
from http import HTTPStatus
from fastapi import Depends, HTTPException
from services.services_usuarios import gerar_hash_usuario, verificar_senha
import jwt
from jwt import DecodeError
from dotenv import load_dotenv
import os
import secrets

load_dotenv()


HASH_FAKE = gerar_hash_usuario("hash_fake")
SECRET_KEY = os.getenv('SECRET_KEY_JWT')
ALGORITHM ="HS256"
esquema = HTTPBearer()


async def autenticar_usuario(email_user: str, senha_user: str ,session: AsyncSession) -> User:

    stmt_email = select(User).where(User.email == email_user)
    user = await session.scalar(stmt_email)

    if not user:
        verificar_senha(senha_user, HASH_FAKE)
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            detail='Credenciais inválidas, tente novamente'
        )

    if verificar_senha(senha_user, user.senha_hash) == False:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            detail='Credenciais inválidas, tente novamente'
        )

    return user

    
def gerar_token_usuario( 
        id_user: int, 
        perfil: str, 
        email: str, 
        empresa_id: int, 
        filial_id:int | None
    ) -> str:

    """ Recebe informações do usuário e retorna um TOKEN JWT """

    payload = {
            "id_user": id_user,
            "perfil": perfil,
            "email": email,
            "empresa_id": empresa_id,
            "filial_id": filial_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=7)
    } 
    
    encoded = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded

def decode_token(token: str) -> dict:

    decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return decode

def get_current_user(token: HTTPAuthorizationCredentials = Depends(esquema)) -> dict:

    credenciais = token.credentials

    credencial = decode_token(credenciais)

    return credencial