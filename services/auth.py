from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios import User
from http import HTTPStatus
from fastapi import HTTPException

HASH_FAKE = ''

async def autenticar_usuario(email_user: str, senha_user: str ,session: AsyncSession) -> User:

    stmt_email = select(User).where(User.email == email_user)
    user_email = await session.scalar(stmt_email)

    if not user_email:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Credenciais inválidas, tente novamente'
        )
    
    


async def gerar_token_usuario():
    pass