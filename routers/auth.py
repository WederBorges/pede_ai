from fastapi import APIRouter, HTTPException
from http import HTTPStatus
router = APIRouter(prefix='auth', tags=["Autenticação"])


router.post('/login', response_model=HTTPStatus.OK)
async def login():
    pass