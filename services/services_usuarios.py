#### Validação rota usuarios ####
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from models.empresas_e_filiais import Filiais

async def validar_filial_e_empresas(session, dados, empresa_id_atual=None):

    empresa_id = dados.empresa_id if dados.empresa_id is not None else empresa_id_atual
    
    stmt = select(Filiais).where(
        Filiais.id == dados.filial_id,
        Filiais.empresa_id == empresa_id)
    
    validacao = await session.scalar(stmt)

    
    if validacao is None:
         raise HTTPException(
            HTTPStatus.NOT_FOUND,
            'Empresa ou filial inexistente'
        )
    print(type(validacao))
    return validacao