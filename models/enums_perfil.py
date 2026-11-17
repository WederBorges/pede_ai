from enum import Enum

class Perfis(str, Enum):
    USUARIO_CHAVE = 'USUARIO_CHAVE'
    USUARIO_APOIO = 'USUARIO_APOIO'
    OPERADOR = 'OPERADOR'
    USUARIO_FILIAL = 'USUARIO_FILIAL'
    USUARIO_CORPORATIVO = 'USUARIO_CORPORATIVO'

GESTAO_DE_ACESSOS = {
    
    Perfis.USUARIO_CHAVE: [
        Perfis.USUARIO_APOIO,
        Perfis.OPERADOR,
        Perfis.USUARIO_CORPORATIVO,
        Perfis.USUARIO_FILIAL],

    Perfis.USUARIO_APOIO: [
        Perfis.OPERADOR,
        Perfis.USUARIO_CORPORATIVO,
        Perfis.USUARIO_FILIAL
    ] 
}
